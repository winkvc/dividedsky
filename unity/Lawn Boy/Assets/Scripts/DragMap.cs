using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mapbox.Unity.Map;

public class DragMap : MonoBehaviour {

	public AbstractMap map;
	public Camera castingCamera;

	private Vector3 targetPoint;

	// Use this for initialization
	void Start () {
		
	}

	Vector3 GetRaycast() {
		Ray ray = castingCamera.ScreenPointToRay(Input.mousePosition);
		RaycastHit hit;
		if (Physics.Raycast(ray, out hit)){
			if (map.gameObject == hit.transform.gameObject) {
				return ray.GetPoint (hit.distance);
			}
		}
		return new Vector3 (0, 0, 0);
	}
	
	// Update is called once per frame
	void Update () {
		// TODO: handle zero values
		if (Input.GetMouseButtonDown(0)) {
			// if left button pressed...
			// set the target positin
			targetPoint = GetRaycast();

		} else if (Input.GetMouseButton(0)) {
			// if it's still pressed... 
			// move the camera such that the point you're pointing to matches the original raycast point.
			// it is pointing to X
			// but you want it pointing to Y
			// so you fake it by adding in Y-X to the camera.
			Vector3 vectorPoint = GetRaycast();
			castingCamera.gameObject.transform.position += (targetPoint - vectorPoint);
		}
	}
}
