using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class PlayerHealth : MonoBehaviour {
	#region Properties
	public Text healthText;
	public float BombDamage = 10.0f;

	private float playerHealth = 100.0f;
	#endregion

	#region Methods
	void Start()
	{
		UpdateHealthText ();
	}

	/// <summary>
	/// Decrements the health of the player.
	/// </summary>
	/// <param name="amount">Amount.</param>
	public void DecrementHealth(float amount)
	{
		playerHealth -= amount;
		UpdateHealthText ();
	}

	/// <summary>
	/// Updates the health text.
	/// </summary>
	public void UpdateHealthText()
	{
		if (healthText != null)
			healthText.text = "Health: " + playerHealth.ToString();
	}

	/// <summary>
	/// Gets the current health value of the player.
	/// </summary>
	/// <returns>The health.</returns>
	public float GetHealth()
	{
		return playerHealth;
	}
	#endregion
}
