using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mapbox.Unity.Utilities;
using Mapbox.Unity.Map;
using Mapbox.Utils;

public class ZoomHandler : MonoBehaviour {

	public AbstractMap _map;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.I)) {
			_map.UpdateMap (_map.CenterLatitudeLongitude, _map.Zoom + 0.5f);
			transform.localScale = new Vector3 (1, 1, 1);
		} else if (Input.GetKeyDown (KeyCode.U)) {
			_map.UpdateMap (_map.CenterLatitudeLongitude, _map.Zoom - 0.5f);
			transform.localScale = new Vector3 (1, 1, 1);
		}
	}
}
