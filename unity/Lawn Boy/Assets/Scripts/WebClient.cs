using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text.RegularExpressions;

public class WebClient : MonoBehaviour {

	// Use this for initialization
	void Start () {
		StartCoroutine (GetStationLocations());
	}

	IEnumerator GetStationLocations() {
		/*
		 * Get the first request to compare against.
		 */

		//string baseURL = "http://127.0.0.1:8000/";
		string baseURL = "https://dividedsky.herokuapp.com/";

		UnityWebRequest firstRequest = UnityWebRequest.Get(baseURL + "station_locations/");
		yield return firstRequest.SendWebRequest();

		if(firstRequest.isNetworkError || firstRequest.isHttpError) {
			Debug.Log(firstRequest.error);
			yield break;
		}
		string firstText = firstRequest.downloadHandler.text;

		/* 
		 * get the second url to get the CSRF token
		 */
		UnityWebRequest loginPage = UnityWebRequest.Get(baseURL + "accounts/login/");
		yield return loginPage.SendWebRequest ();
		if(loginPage.isNetworkError || loginPage.isHttpError) {
			Debug.Log(loginPage.error);
			yield break;
		}

		// get the csrf cookie
		string SetCookie = loginPage.GetResponseHeader ("set-cookie");
		Regex rxCookie = new Regex("csrftoken=(?<csrf_token>.{64});");
		MatchCollection cookieMatches = rxCookie.Matches (SetCookie);
		string csrfCookie = cookieMatches[0].Groups ["csrf_token"].Value;

		// get the middleware value
		string loginPageHtml = loginPage.downloadHandler.text;
		Regex rxMiddleware = new Regex("name='csrfmiddlewaretoken' value='(?<csrf_token>.{64})'");
		MatchCollection middlewareMatches = rxMiddleware.Matches(loginPageHtml);
		string csrfMiddlewareToken = middlewareMatches[0].Groups ["csrf_token"].Value;
			
		/*
		 * Make a login request.
		 */
		// set up the post form
		WWWForm form = new WWWForm();
		form.AddField("csrfmiddlewaretoken", csrfMiddlewareToken);
		form.AddField("username", "fake");
		form.AddField("password", "fakepass");
		form.AddField("next", "/");

		// create the request
		UnityWebRequest doLogin = UnityWebRequest.Post(baseURL + "accounts/login/", form);
		doLogin.chunkedTransfer = false; // apparently django doesn't support chunked transfer
		doLogin.redirectLimit = 0; // give me the 302 so I can get the right cookies
		doLogin.SetRequestHeader ("referer", baseURL + "accounts/login/"); // avoid CSRF problems
		doLogin.SetRequestHeader ("cookie", "csrftoken=" + csrfCookie);
		doLogin.SetRequestHeader ("X-CSRFToken", csrfCookie);

		// send request
		yield return doLogin.SendWebRequest ();

		// get reply
		Debug.Log (doLogin.responseCode); // did it work [aka give me a 302]
		string loginCookies = doLogin.GetResponseHeader ("set-cookie"); // parse for new cookies
		Debug.Log(loginCookies);

		// parse for cookies
		/* sessionid=6vzgfwmnapf2ou4wvkplgf7fvy429aem; expires=Sun, 27-May-2018 08:39:03 GMT; 
		 * httponly; Max-Age=1209600; Path=/; secure,csrftoken=11X5eIkIbwg4JGb3jpqh1exfNmJzKVmN1G4TbxcapBBbaYyxrhPwxNfOANpwlVkk; 
		 * expires=Sun, 12-May-2019 08:39:03 GMT; Max-Age=31449600; Path=/
		 */
		MatchCollection newCookieMatches = rxCookie.Matches (loginCookies);
		string newCsrfCookie = newCookieMatches[0].Groups ["csrf_token"].Value;
		Regex rxSessionCookie = new Regex("sessionid=(?<sessionid>.{32});");
		MatchCollection sessionMatches = rxSessionCookie.Matches (loginCookies);
		string sessionCookie = sessionMatches[0].Groups ["sessionid"].Value;

		Debug.Log (newCsrfCookie);
		Debug.Log (sessionCookie);


		/* 
		 * remake the first request and see if something changed...
		 */

		UnityWebRequest secondRequest = UnityWebRequest.Get (baseURL + "station_locations/");
		string fullCookieString = "sessionid=" + sessionCookie + "; csrftoken=" + newCsrfCookie;
		secondRequest.SetRequestHeader("cookie", fullCookieString);
		//sessionid=6jr8yeh994bmnnmafq2mj057xvnqvvwn; csrftoken=BzSmhQspD4be3K3eoioUvygtvWGIbj9TUwRwsxxlVX8tGCCfDVYfSmXSKuMu9Gim
		yield return secondRequest.SendWebRequest();

		if(secondRequest.isNetworkError || secondRequest.isHttpError) {
			Debug.Log(secondRequest.error);
			yield break;
		}

		string secondText = secondRequest.downloadHandler.text;
		Debug.Log (firstText); 
		Debug.Log (secondText); 
	}
}
