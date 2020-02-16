using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;

public class SceneManager : MonoBehaviour {
	#region Properties
	public Text countText;
	public Text winText;
	public int reloadTime = 2;
	public List<GameObject> debrisPieces = new List<GameObject>();
	public int SpawnCount = 12;
	public Vector2 SpawnWidthBounds = new Vector2(-7.0f, 7.0f);
	public Vector2 SpawnLengthBounds = new Vector2 (-7.0f, 7.0f);
	public float SpawnHeightBounds = 1.0f; 
	
	#endregion

	#region Methods
	void Start()
	{
		if (winText != null)
			winText.text = "";

		SpawnDebris ();
	}

	/// <summary>
	/// Sets the count text to the number of attached debris pieces.
	/// </summary>
	/// <param name="count">Count.</param>
	public void SetCountText(int count)
	{	
		if (countText != null)
			countText.text = "Count: " + count.ToString ();
		
		if (count >= SpawnCount)
		{
			StartCoroutine(PlayerWins());
		}
	}

	/// <summary>
	/// If the player wins set the win text
	/// and reload the level after a set period of seconds.
	/// </summary>
	/// <returns>The wins.</returns>
	IEnumerator PlayerWins()
	{
		if (winText != null)
			winText.text = "You win!";

		yield return new WaitForSeconds(reloadTime);
		ReloadLevel ();
	}

	/// <summary>
	/// Reloads the scene after the player loses.
	/// </summary>
	/// <returns>The lose.</returns>
	public IEnumerator PlayerLose()
	{
		if (winText != null)
			winText.text = "You Lose!";

		yield return new WaitForSeconds (reloadTime);
		ReloadLevel ();
	}

	/// <summary>
	/// Reloads the currently loaded level.
	/// </summary>
	private void ReloadLevel()
	{
		Application.LoadLevel (Application.loadedLevel);
	}

	/// <summary>
	/// Spawns the debris in a random location.
	/// </summary>
	private void SpawnDebris()
	{
		if (debrisPieces.Count == 0)
			return;

		GameObject debrisRoot = new GameObject ("Debris Root");

		for (int spawnCounter = 0; spawnCounter < SpawnCount; spawnCounter++) {
			int pieceIndex = Random.Range(0, debrisPieces.Count - 1);

			GameObject piece = debrisPieces[pieceIndex];

			if (piece != null)
			{
				GameObject debrisInstance = Instantiate(piece);
				debrisInstance.transform.parent = debrisRoot.transform;

				// generate random locations for the spawned pieces
				float randomX = Random.Range(SpawnWidthBounds.x, SpawnWidthBounds.y);
				float randomY = Random.Range(0.0f, SpawnHeightBounds);
				float randomZ = Random.Range(SpawnLengthBounds.x, SpawnLengthBounds.y);

				Vector3 translateVector = new Vector3(randomX, randomY, randomZ);

				debrisInstance.transform.Translate(translateVector);
			}
		}

	}
	#endregion
}
