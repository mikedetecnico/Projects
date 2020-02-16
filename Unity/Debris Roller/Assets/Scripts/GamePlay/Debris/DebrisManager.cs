using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[RequireComponent (typeof (Rigidbody))]
public class DebrisManager : MonoBehaviour {
	#region Properties
	public Vector3 debrisRotation = new Vector3(15, 30, 45);

	private int numAttached = 0;
	#endregion

	#region Methods
	void Update()
	{
		RotateDebris ();
	}

	/// <summary>
	/// Gets the debris count.
	/// </summary>
	/// <returns>The debris count.</returns>
	public static int GetDebrisCount()
	{
		GameObject[] debrisPieces = GameObject.FindGameObjectsWithTag (TagManager.Debris);

		int debrisCount = debrisPieces.Length;

		return debrisCount;
	}

	/// <summary>
	/// Attachs the debris to the player object.
	/// </summary>
	/// <param name="debrisPiece">Debris piece.</param>
	/// <param name="player">Player.</param>
	public void AttachDebris(GameObject debrisPiece, GameObject player)
	{
		// set the debris piece's parent to be the player.  This will
		// attach the debris piece to the location where it had
		// contact with the player.
		debrisPiece.transform.SetParent(player.transform);

		Collider debrisCollider = debrisPiece.GetComponent<Collider> ();

		debrisCollider.enabled = false;

		// since the attached debris pieces are children of the player
		// get the child count under the player to find the number of pieces
		// attached
		List<GameObject> debrisChildren = new List<GameObject> ();

		for (int childIndex = 0; childIndex < player.transform.childCount; childIndex++) {
			GameObject childObj = player.transform.GetChild(childIndex).gameObject;
			if (childObj.tag == TagManager.Debris)
			{
				debrisChildren.Add(childObj);
			}
		}

		numAttached = debrisChildren.Count;
	}

	/// <summary>
	/// Gets the number of attached pieces.
	/// </summary>
	/// <returns>The number attached pieces.</returns>
	public int GetNumAttached()
	{
		return numAttached;
	}

	/// <summary>
	/// Rotates the debris using the debris Rotation vector,
	/// which can be set in the inspector.
	/// </summary>
	private void RotateDebris()
	{
		transform.Rotate (debrisRotation * Time.deltaTime);
	}
	#endregion

}
