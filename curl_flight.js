const https = require('https');
const jq = require('jquery-jsdom');
 
var args = process.argv.slice(2);
var url = '';

function parseData(html) {
    console.log(html);
}

for (var i = 0; i < args.length; i++) {
    if (args[i] === '--url') {
        url = args[i + 1];
        break;
    }
}

if (url) {
    https.get(url, (resp) => {
        let data = '';

        // A chunk of data has been recieved.
        resp.on('data', (chunk) => {
            data += chunk;
        });

        // The whole response has been received. Print out the result.
        resp.on('end', () => {
            parseData(data);
        });

    }).on('error', (err) => {
        console.log('Error: ' + err.message);
    });
}


www.google.com/async/flights/search?async=data:%5B%5B%5B%5B%5B%5Bnull%2C%5B%5B%22%2Fm%2F02_n7%22%2C4%5D%5D%5D%2C%5Bnull%2C%5B%5B%22BZN%22%2C0%5D%5D%5D%2C%5B%222020-01-11%22%5D%5D%2C%5B%5Bnull%2C%5B%5B%22BZN%22%2C0%5D%5D%5D%2C%5Bnull%2C%5B%5B%22%2Fm%2F02_n7%22%2C4%5D%5D%5D%2C%5B%222020-01-15%22%5D%5D%5D%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C1%2Cnull%2C2%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%5D%2C%5B%5B%5Bnull%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2Cnull%2C%5B%5D%2C%5B%5D%5D%2C%5Bnull%2C%5B%5D%2C%5B%5D%2C%5B%5D%2C%5B%5D%2Cnull%2C%5B%5D%2C%5B%5D%5D%5D%5D%2Cnull%2C%22USD%22%2C1%2C%5B%5D%5D%2C%5B0%5D%5D,s:s,tfg-bgr:%5B%22!HR6lHj9C6Hein_9L_R5YnfVDgE9EmCQCAAAAN1IAAAAJmQGTwQN3PvwWZNvYd4HMWByoNCmygBioNH0KHeMzTg3zT__t46hHogAda8OaO-nEj9FpftdXY1y8HoxSTYxpYyBzRAvaW5FrmbCC4WnG6qC-pfnBbliWYUPSRknXCdgMID-vTgG1kIK_U3hQs8NLjTokU9EZ_dPiSXFbDeEbFv1KwVup7HkmEn_HUhtw4nz6as03ar5dTNxHf19oS6N5UzKmo-brJqdXtoaVLw7HkgWMgXXV9U89iqcfEMoIFwjxFVFYAj9N9UJXIvJIo4lr5TyBXIqo4v1IK2I6_zlSYBJNOg_Zt2FMg1kWfpSVC6Q0lBUXVE1mzr5HX85lWT3nR49UHEpgYetX8X7j2RCWTKIKlwAy0VZOTcWgYAB2WEQtleR1bT-0_iONaJQJfnWJ1Is8V6oNcoMptze96RLhuzbxg0khJAF6fBwEpLqSOEsvBPmLHduiwOdD74ooyr5bSWSqtDfaZ3EyY6dTek_yWU0glI9YSPyfySmogaIZxhLOoX5yNyBTOQ0P96XAwM7d8Vd3fFA_zA%22%2Cnull%2Cnull%2C10%2C62%2Cnull%2Cnull%2C0%5D,_fmt:jspb






