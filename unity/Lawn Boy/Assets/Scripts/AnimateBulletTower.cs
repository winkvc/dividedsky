using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnimateBulletTower : MonoBehaviour {

	// turret spinning vars
	public GameObject turret;
	private float angleDelta;
	private int whenToRotate;
	private const int rotatePeriod = 1000;
	private const int rotateDuration = 100;

	void SetupTurretRotation () {
		whenToRotate = (int)(Random.value * rotatePeriod);
		turret.transform.Rotate (0f, Random.value * 360f - 180f, 0f);
	}

	// Use this for initialization
	void Start () {
		SetupTurretRotation ();
	}

	void UpdateTurretRotation () {
		int stepInBarrelRotateLoop = (Time.frameCount + whenToRotate) % rotatePeriod;

		// every 1000 frames, get the first 100
		if (stepInBarrelRotateLoop < rotateDuration) {
			if (stepInBarrelRotateLoop == 0) {
				// if it's the very first
				// randomly choose an angleDelta to apply at each step
				//Debug.Log(gameObject.GetHashCode());
				angleDelta = Random.value * (360f / rotateDuration) - (180f / rotateDuration);
			}

			// now move that delta along the y rotation axis.
			turret.transform.Rotate(0f, angleDelta, 0f);
		}
	}
	
	// Update is called once per frame
	void Update () {
		UpdateTurretRotation ();
	}
}
