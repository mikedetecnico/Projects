using UnityEngine;
using System.Collections;

[RequireComponent (typeof (Camera))]
public class CameraController : MonoBehaviour {
	#region Properties
	public GameObject player;

	private Vector3 offset = new Vector3();
	#endregion

	#region Methods
	void Start()
	{
		if (player != null)
			SetCameraOffset (player.transform.position);
	}

	void LateUpdate()
	{
		if (player != null)
			UpdatePosition (player.transform.position);
	}

	/// <summary>
	/// Sets the camera offset.
	/// </summary>
	/// <param name="playerPos">Player position.</param>
	public void SetCameraOffset(Vector3 playerPos)
	{
		// the camera will be offset based on the vector from the camera
		// to the player so that it always follows the current player position
		// and disregards the rotation.
		offset = transform.position - playerPos;
	}

	/// <summary>
	/// Updates the position.
	/// </summary>
	/// <param name="playerPos">Player position.</param>
	private void UpdatePosition(Vector3 playerPos)
	{
		transform.position = playerPos + offset;
	}
	#endregion
}
