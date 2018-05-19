using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Mapbox.Unity.Utilities;
using Mapbox.Unity.Map;
using Mapbox.Utils;
using UnityEngine.Networking;
using Newtonsoft.Json;
using System;

public class ScratchScript : MonoBehaviour {

	// created with http://json2csharp.com/
	public class Position
	{
		public double lat { get; set; }
		public double lng { get; set; }
	}

	public class Datum
	{
		public string icon { get; set; }
		public int db_id { get; set; }
		public Position position { get; set; }
		public int health { get; set; }
		public string station_type { get; set; }
		public int gathered_energy { get; set; }
	}

	public class RootObject
	{
		public List<Datum> data { get; set; }
	}

	public AbstractMap _map;

	[Serializable]
	public class NameToGameObject
	{
		public string sprite;
		public GameObject station;
	}

	public NameToGameObject[] stations;

	private RootObject jsonResult;

	private bool hasMapLoaded = false;
	private bool hasStationsJsonLoaded = false;

	// Use this for initialization
	void Start () {
		_map.OnInitialized += MarkMapInitialized;
		StartCoroutine (GetStationLocations());
	}

	IEnumerator GetStationLocations() {
		//Debug.Log ("Sending request...");
		UnityWebRequest www = UnityWebRequest.Get("http://dividedsky.herokuapp.com/station_locations/");
		yield return www.SendWebRequest();

		if(www.isNetworkError || www.isHttpError) {
			Debug.Log(www.error);
		}
		else {
			// Show results as text
			string text = www.downloadHandler.text;
			jsonResult = JsonConvert.DeserializeObject<RootObject>(text);
			hasStationsJsonLoaded = true;
			PossiblyLoadStations ();
		}
	}

	void MarkMapInitialized() {
		hasMapLoaded = true;
		PossiblyLoadStations ();
	}

	void PossiblyLoadStations () {
		// check both values - if not, wait for another call.
		if (hasMapLoaded && hasStationsJsonLoaded) {
			LoadStations ();
		} else {
			//Debug.Log ("map:");
			//Debug.Log (hasMapLoaded);
			//Debug.Log ("json:"); 
			//Debug.Log (hasStationsJsonLoaded);
		}
	}

	void LoadStations() {
		//Debug.Log ("Loadstations");
		// assuming both things have loaded.
		foreach (Datum datum in jsonResult.data) {
			Vector2d latLon = new Vector2d((float)datum.position.lat, (float)datum.position.lng);
			Vector2d unityXZ = Conversions.GeoToWorldPosition (latLon, _map.CenterMercator, _map.WorldRelativeScale);
			Vector3 unityWorld = new Vector3 ((float)unityXZ.x, transform.position.y, (float)unityXZ.y);
			foreach (NameToGameObject description in stations) {
				if ( datum.icon.EndsWith(description.sprite)) {
					Instantiate (description.station, unityWorld, new Quaternion ());
					break;
				}
			}
			
		}
	}

	void SetPosition() {
		// create some object at 37.425177, -122.171306
		Vector2d latLon = new Vector2d(37.425177f, -122.171306f);
		Vector2d unityWorld = Conversions.GeoToWorldPosition (latLon, _map.CenterMercator, _map.WorldRelativeScale);
		//Debug.Log (unityWorld);
		transform.position = new Vector3 ((float)unityWorld.x, transform.position.y, (float)unityWorld.y);
	}
	
	// Update is called once per frame
	void Update () {
		
	}


}
