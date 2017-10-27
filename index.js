const functions = require('firebase-functions');
var bodyparser = require('body-parser');
var queryString = require('querystring');

// The Firebase Admin SDK to access the Firebase Realtime Database. 
const admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);


// Take the text parameter passed to this HTTP endpoint and insert it into the
// Realtime Database under the path /messages/:pushId/original



/**************************************************************************************************/
exports.sendMessenger = functions.https.onRequest((req, res) => {

const original = req.body;

//console.log(req);
//console.log(original);
var all = JSON.parse(req.body);
console.log(all.A);
	
  // Push the new message into the Realtime Database using the Firebase Admin SDK.
  admin.database().ref('/Sender').push({original: all.data}).then(snapshot => {
  	res.sendStatus(200);
  
  });
});

/**************************************************************************************************

								RECEBIMENDO DE PACOTE DO TIPO 1

**************************************************************************************************/
exports.sendMessengerType1 = functions.https.onRequest((req, res) => {
  // Grab the text parameter.
const original = req.body;

//console.log(req);
//console.log(original);
var all = JSON.parse(req.body);
const type = parseInt(all.A,16);
const resp = parseInt(all.B,16);
const bpm = parseInt(all.C,16);
const oxi = parseInt(all.D,16);
const sis = parseInt(all.E,16);
const dias = parseInt(all.F,16);
const ecg = parseInt(all.G+all.H+all.I+all.J,16); //4bytes
const sintom = parseInt(all.K,16);

console.log(all.A);
console.log(type);

	
if(type == 1){
	  // Push the new message into the Realtime Database using the Firebase Admin SDK.
	  console.log("ok");

  	  admin.database().ref('/Type1').push({

  	  	original: all.data,
  	  	Air: resp,
  	  	BPM: bpm,
  	  	Spo2: oxi,
  	  	Sistolica: sis,
  	  	Diastolica: dias,
  	  	ECG: ecg,
  	  	Sintoma: sintom

  	  }).then(snapshot => {
  		res.sendStatus(200);
  
  });
}

else {
	console.log("not mine");
	res.sendStatus(200);
}
});

/**************************************************************************************************
								
								RECEBIMENDO DE PACOTE DO TIPO 2

**************************************************************************************************/
exports.sendMessengerType2 = functions.https.onRequest((req, res) => {
  // Grab the text parameter.
const original = req.body;

//console.log(req);
//console.log(original);
var all = JSON.parse(req.body);
const type = parseInt(all.A,16);
const altura = parseInt(all.B,16);
const idade = parseInt(all.C,16);
const sexo = parseInt(all.D,16);
const causa = parseInt(all.E,16);
const peso = parseInt(all.F,16);
const temp = parseInt(all.G+all.H+all.I+all.J,16); //4bytes

console.log(all.A);
console.log(type);

	
if(type == 2){
	  // Push the new message into the Realtime Database using the Firebase Admin SDK.
	  console.log("ok");

  	  admin.database().ref('/Type2').push({

  	  	original: all.data,
  	  	Altura: altura,
  	  	Idade: idade,
  	  	Sexo: sexo,
  	  	Causa: causa,
  	  	Peso: peso,
  	  	Temperatura: temp

  	  }).then(snapshot => {
  		res.sendStatus(200);
  
  });
}

else {
	console.log("not mine");
	res.sendStatus(200);
}
});

/**************************************************************************************************

							RECEBIMENDO DE PACOTE DO TIPO 3

**************************************************************************************************/
exports.sendMessengerType3 = functions.https.onRequest((req, res) => {
  // Grab the text parameter.
const original = req.body;

//console.log(req);
//console.log(original);
var all = JSON.parse(req.body);
const type = parseInt(all.A,16);
const gps = parseInt(all.B+all.C+all.D+all.E+all.F+all.G,16);

console.log(all.A);
console.log(type);

	
if(type == 3){
	  // Push the new message into the Realtime Database using the Firebase Admin SDK.
	  console.log("ok");

  	  admin.database().ref('/Type3').push({

  	  	original: all.data,
  	  	GPS: gps  	  	

  	  }).then(snapshot => {
  		res.sendStatus(200);
  
  });
}

else {
	console.log("not mine");
	res.sendStatus(200);
}
});

/**************************************************************************************************/