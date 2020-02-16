using UnityEngine;
using UnityEngine.UI;
using System.Collections;

[RequireComponent (typeof (Rigidbody))]
public class PlayerController : MonoBehaviour {
	#region Properties
	public float speed;
	public string HorizontalKey = "Horizontal";
	public string VerticalKey = "Vertical";
	public string JumpKey = "Jump";
	public float JumpHeight = 1.0f;

	private Rigidbody rb;
	private SceneManager sm = null;
	private PlayerHealth health;
	#endregion

	#region Methods
	void Start()
	{
		rb = GetComponent<Rigidbody> ();

		GameObject sm_object = GameObject.FindGameObjectWithTag (TagManager.GameController);

		if (sm_object != null) {
			sm = sm_object.GetComponent<SceneManager> ();
		}

		sm.SetCountText (0);

		health = GetComponent<PlayerHealth> ();
	}

	void FixedUpdate()
	{
		// move based on the left/right and forward/back keys
		MovePlayer ();

		// jump if the player hits the jump key
		if (Input.GetButtonDown (JumpKey)) {
			Jump();
		}

		UpdateHealth (Time.deltaTime);
	}

	void OnTriggerEnter(Collider other)
	{
		if (other.gameObject.CompareTag (TagManager.Debris)) {
			PickupDebris (other.gameObject);
		} 

		else if (other.gameObject.CompareTag (TagManager.Bomb)) {
			BombHit();

			other.gameObject.SetActive(false);
		}
	}

	/// <summary>
	/// Updates the health of the player based on delta time.
	/// </summary>
	private void UpdateHealth(float damage)
	{
		if (health.GetHealth () > 0.0f) {
			health.DecrementHealth (damage);
		}
		
		// check the players health to make sure it is not at or close to 0
		if (health.GetHealth () < Mathf.Epsilon) {
			StartCoroutine(sm.PlayerLose());
		}
	}

	/// <summary>
	/// Moves the player forward/back and left/right.
	/// </summary>
	private void MovePlayer()
	{
		float moveHorizontal = Input.GetAxis (HorizontalKey);
		float moveVertical = Input.GetAxis (VerticalKey);
		
		Vector3 movement = new Vector3 (moveHorizontal, 0.0f, moveVertical);
		
		rb.AddForce (movement * speed);
	}

	/// <summary>
	/// Jump!
	/// </summary>
	private void Jump()
	{
		rb.AddForce(Vector3.up * JumpHeight);
	}

	/// <summary>
	/// Pickups the debris and attaches it to the player object
	/// </summary>
	/// <param name="debrisPieces">Debris pieces.</param>
	private void PickupDebris(GameObject debrisPiece)
	{
		DebrisManager dm = debrisPiece.GetComponent<DebrisManager>();

		if (dm != null) {
			dm.AttachDebris (debrisPiece, gameObject);
		
			sm.SetCountText (dm.GetNumAttached ());
		}
	}

	private void BombHit()
	{
		// if the amount of bomb damage will take the player's 
		// health below 0, then only decrement the health to 0
		// instead of the full amount
		if (health.GetHealth() > health.BombDamage) 
			UpdateHealth(health.BombDamage);
		
		else {
			UpdateHealth(health.GetHealth() - Mathf.Epsilon);
		}
	}
	#endregion
}
