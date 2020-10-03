const fetch = require("node-fetch");
const airtableAuth = "Bearer keyHmyS9AODHkZSLY";

async function scrapeStockbitTrending() {
  try {
    let retry = 0;
    let resData = "";

    while (retry <= 5) {
      let token = await getAuth("Stockbit Access Token");
      let res = await fetch("https://api.stockbit.com/v2.3/company/trending", {
        headers: {
          Authorization: token
        }
      });

      if (!res.ok) throw `Stockbit API not 200 - ${res.status}`;

      resData = await res.json();
      if (resData["error"] == "UnAuthorized") {
        if (retry < 3) await refreshStockbitToken();
        else await loginStockbit();
        retry++;
      } else {
        retry = 999;
      }
    }
    if (resData["error"])
      throw `Stockbit API error: ${resData["error"]} - ${resData["message"]}`;

    let data = resData["data"];
    let stocks = data.map(d => d["symbol"]);
    let points = data.map(d => d["point"]);
    let record = { Time: new Date().toISOString() };
    for (let i = 1; i <= data.length; i++) {
      record["S" + i] = stocks[i - 1];
      record["P" + i] = parseFloat(points[i - 1]);
    }

    res = await fetch(
      "https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Stockbit%20Trending",
      {
        method: "POST",
        headers: {
          Authorization: airtableAuth,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ fields: record })
      }
    );

    if (!res.ok) {
      let body = await res.text();
      throw `Airtable API not 200 on POST Stockbit Trending - ${body}`;
    }

    log(
      "Stockbit Trending",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 3600 * 1000)),
      ""
    );
  } catch (error) {
    log(
      "Stockbit Trending",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 3600 * 1000)),
      error
    );
  }
}

async function scrapeIdxTopGainersAndLosers(threshold = 0) {
  try {
    let res = await fetch(
      "https://www.idx.co.id/umbraco/Surface/Home/GetTopGainer?resultCount=10000"
    );

    if (!res.ok) throw `IDX API not 200 - ${res.status}`;

    let jsonString = await res.json();
    let data = JSON.parse(jsonString);
    data = data.filter(d => d["Frequency"] > threshold);
    let stocks = data.map(d => d["Code"]);
    let percents = data.map(d => d["Percent"]);
    let freqs = data.map(d => d["Frequency"]);
    let count = 15;

    // Top Gainers
    let gainers = { Time: new Date().toISOString() };
    for (let i = 1; i <= count; i++) {
      gainers["S" + i] = stocks[i - 1].trim();
      gainers["C" + i] = parseFloat(percents[i - 1]);
      gainers["F" + i] = parseInt(freqs[i - 1]);
    }

    res = await fetch(
      "https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Top%20Gainers",
      {
        method: "POST",
        headers: {
          Authorization: airtableAuth,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ fields: gainers })
      }
    );

    if (!res.ok) {
      let body = await res.text();
      throw `Airtable API not 200 on POST IDX Top Gainers - ${body}`;
    }

    log(
      "IDX Top Gainers",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 24 * 3600 * 1000)),
      ""
    );

    // Top Losers
    let losers = { Time: new Date().toISOString() };
    let totalLength = data.length;
    for (let i = 1; i <= count; i++) {
      losers["S" + i] = stocks[totalLength - i].trim();
      losers["C" + i] = parseFloat(percents[totalLength - i]);
      losers["F" + i] = parseInt(freqs[totalLength - i]);
    }

    res = await fetch(
      "https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Top%20Losers",
      {
        method: "POST",
        headers: {
          Authorization: airtableAuth,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ fields: losers })
      }
    );

    if (!res.ok) {
      let body = await res.text();
      throw `Airtable API not 200 on POST IDX Top Losers - ${body}`;
    }

    log(
      "IDX Top Losers",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 24 * 3600 * 1000)),
      ""
    );
  } catch (error) {
    log(
      "IDX Top Gainers and Losers",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 24 * 3600 * 1000)),
      error
    );
  }
}

async function scrapeIdxMostActive() {
  try {
    let res = await fetch(
      "https://www.idx.co.id/umbraco/Surface/Home/GetTopFrequent?resultCount=15"
    );

    if (!res.ok) throw `IDX API not 200 - ${res.status}`;

    let jsonString = await res.json();
    let data = JSON.parse(jsonString);
    let stocks = data.map(d => d["Code"]);
    let percents = data.map(d => d["Percent"]);
    let freqs = data.map(d => d["Frequency"]);
    let record = { Time: new Date().toISOString() };
    for (let i = 1; i <= data.length; i++) {
      record["S" + i] = stocks[i - 1].trim();
      record["C" + i] = parseFloat(percents[i - 1]);
      record["F" + i] = parseInt(freqs[i - 1]);
    }

    res = await fetch(
      "https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Most%20Active",
      {
        method: "POST",
        headers: {
          Authorization: airtableAuth,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ fields: record })
      }
    );

    if (!res.ok) {
      let body = await res.text();
      throw `Airtable API not 200 on POST IDX Most Active - ${body}`;
    }

    log(
      "IDX Most Active",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 24 * 3600 * 1000)),
      ""
    );
  } catch (error) {
    log(
      "IDX Most Active",
      new Date(),
      new Date(new Date().setTime(new Date().getTime() + 24 * 3600 * 1000)),
      error
    );
  }
}

async function refreshStockbitToken() {
  let refresh = await getAuth("Stockbit Refresh Token");
  let res = await fetch("https://api.stockbit.com/v2.3/login/refresh", {
    headers: {
      Authorization: refresh
    }
  });

  if (!res.ok) {
    let body = await res.text();
    throw `Stockbit refresh not 200 - ${body}`;
  }

  let data = await res.json();
  let access = "Bearer " + data["data"]["access_token"];
  refresh = "Bearer " + data["data"]["refresh_token"];
  await setAuth("Stockbit Access Token", access);
  await setAuth("Stockbit Refresh Token", refresh);
}

async function loginStockbit() {
  let res = await fetch("https://api.stockbit.com/v2.3/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: "user=alala@mailinator.com&password=alala"
  });

  if (!res.ok) {
    let body = await res.text();
    throw `Stockbit login not 200 - ${body}`;
  }

  let data = await res.json();
  let access = "Bearer " + data["data"]["access_token"];
  refresh = "Bearer " + data["data"]["refresh_token"];
  await setAuth("Stockbit Access Token", access);
  await setAuth("Stockbit Refresh Token", refresh);
}

async function getAuth(key) {
  const res = await fetch(
    `https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Auth?filterByFormula=Key='${key}'`,
    {
      headers: {
        Authorization: airtableAuth
      }
    }
  );

  if (!res.ok) {
    let body = await res.text();
    throw `Airtable API not 200 on getting ${key} Auth - ${body}`;
  }

  let data = await res.json();
  let record = data["records"][0];
  let value = record["fields"]["Value"];
  return value;
}

async function setAuth(key, value) {
  let res = await fetch(
    `https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Auth?filterByFormula=Key='${key}'`,
    {
      headers: {
        Authorization: airtableAuth
      }
    }
  );

  if (!res.ok) {
    let body = await res.text();
    throw `Airtable API not 200 on getting ${key} Auth - ${body}`;
  }

  let data = await res.json();
  let record = data["records"][0];
  let id = record["id"];

  res = await fetch(
    `https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Auth/${id}`,
    {
      method: "PATCH",
      headers: {
        Authorization: airtableAuth,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ fields: { Value: value } })
    }
  );

  if (!res.ok) {
    let body = await res.text();
    throw `Airtable API not 200 on setting ${key} Auth - ${body}`;
  }
}

async function log(name, last, next, message) {
  let res = await fetch("https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Log", {
    headers: {
      Authorization: airtableAuth
    }
  });

  if (!res.ok) {
    let body = await res.text();
    throw `Airtable API not 200 on getting Stockbit Auth - ${body}`;
  }

  let data = await res.json();
  let records = data["records"];
  record = records.filter(r => r["fields"]["Name"] == name)[0];
  let id = record["id"];

  res = await fetch("https://api.airtable.com/v0/apppzlsQkO8FTOzwK/Log/" + id, {
    method: "PUT",
    headers: {
      Authorization: airtableAuth,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      fields: {
        Name: name,
        Last: last,
        Next: next,
        Message: message
      }
    })
  });
}