const clientId = "7fe6675024d54a34b4fbe8df31280d5d";
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

async function main() {
  if (!code) {
    redirectToAuthCodeFlow(clientId);
  } else {
    const accessToken = await getAccessToken(clientId, code);
    const profile = await fetchProfile(accessToken);
    populateUI(profile);
    const topSongs = await fetchTopSongs(accessToken);
    displayTopSongs(topSongs);
    const recommendations = await fetchVinylRecommendations(accessToken);
    displayVinylRecommendations(recommendations);
  }
}

main();


// TODO: Redirect to Spotify authorization page
export async function redirectToAuthCodeFlow(clientId) {
    const verifier = generateCodeVerifier(128);
    const challenge = await generateCodeChallenge(verifier);

    localStorage.setItem("verifier", verifier);

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("response_type", "code");
    params.append("redirect_uri", "https://spot-vinyl.herokuapp.com/callback");
        params.append("scope", "user-read-private user-read-email user-top-read");
        params.append("code_challenge_method", "S256");
        params.append("code_challenge", challenge);

        document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
    }
function generateCodeVerifier(length) {
    let text = '';
    let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
async function generateCodeChallenge(codeVerifier) {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, [...new Uint8Array(digest)]))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}
export async function getAccessToken(clientId, code) {
    const verifier = localStorage.getItem("verifier");

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("grant_type", "authorization_code");
    params.append("code", code);
    params.append("redirect_uri", "https://spot-vinyl.herokuapp.com/callback");
    params.append("code_verifier", verifier);

    const result = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params
    });

    const { access_token } = await result.json();
    return access_token;
}
async function fetchProfile(token) {
    const result = await fetch("https://api.spotify.com/v1/me", {
        method: "GET", headers: { Authorization: `Bearer ${token}` }
    });

    return await result.json();


}
// async function fetchTopSongs(token) {
//     const result = await fetch("https://api.spotify.com/v1/me/top/tracks", {
//         method: "GET",
//         headers: { Authorization: `Bearer ${token}` },
//     });
//
//     return await result.json();
// }
// function displayTopSongs(topSongs) {
//     const container = document.getElementById("topSongsContainer");
//     const table = document.createElement("table");
//     table.classList.add("top-songs-table");
//
//     const headerRow = document.createElement("tr");
//     ["Track Name", "Artist"].forEach((headerText) => {
//         const headerCell = document.createElement("th");
//         headerCell.innerText = headerText;
//         headerRow.appendChild(headerCell);
//     });
//     table.appendChild(headerRow);
//
//     topSongs.items.forEach((song) => {
//         const row = document.createElement("tr");
//
//         const trackNameCell = document.createElement("td");
//         trackNameCell.innerText = song.name;
//         row.appendChild(trackNameCell);
//
//         const artistNameCell = document.createElement("td");
//         artistNameCell.innerText = song.artists[0].name;
//         row.appendChild(artistNameCell);
//
//         table.appendChild(row);
//     });
//
//     container.appendChild(table);
// }
// async function fetchVinylRecommendations(token) {
//     console.log('fetchVinylRecommendations called');
//     const response = await fetch("https://spot-vinyl.herokuapp.com/api/vinyl-recommendations", {
//         method: "GET",
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${token}`
//         },
//     });
//     const recommendations = await response.json();
//     console.log('Received recommendations:', recommendations);
//     return recommendations; // Return the recommendations
// }
// function displayVinylRecommendations(recommendations) {
//     const container = document.getElementById("vinylRecommendationsContainer");
//
//     const recommendationsContainer = document.createElement("div");
//     recommendationsContainer.classList.add("recommendations-container");
//
//     recommendations.forEach((recommendation) => {
//         const discogsUrl = recommendation[0];
//         const imageUrl = recommendation[1];
//         const lowestPrice = recommendation[2];
//
//         const vinylElement = document.createElement("div");
//         vinylElement.classList.add("vinyl-recommendation");
//
//         const imageElement = document.createElement("img");
//         imageElement.src = imageUrl;
//         vinylElement.appendChild(imageElement);
//
//         const infoElement = document.createElement("div");
//         infoElement.classList.add("vinyl-info");
//         const priceElement = document.createElement("p");
//         priceElement.innerText = `Lowest: $${lowestPrice.toFixed(2)}`;
//         infoElement.appendChild(priceElement);
//         const discogsLink = document.createElement("a");
//         discogsLink.href = discogsUrl;
//         discogsLink.innerText = "Discogs";
//         infoElement.appendChild(discogsLink);
//
//
//
//         vinylElement.appendChild(infoElement);
//         recommendationsContainer.appendChild(vinylElement);
//     });
//
//     container.appendChild(recommendationsContainer);
// }

function populateUI(profile) {
    document.getElementById("displayName").innerText = profile.display_name;
    if (profile.images[0]) {
        const profileImage = new Image(200, 200);
        profileImage.src = profile.images[0].url;
        document.getElementById("avatar").appendChild(profileImage);
        document.getElementById("imgUrl").innerText = profile.images[0].url;
    }
    document.getElementById("id").innerText = profile.id;
    document.getElementById("email").innerText = profile.email;
    document.getElementById("uri").innerText = profile.uri;
}
