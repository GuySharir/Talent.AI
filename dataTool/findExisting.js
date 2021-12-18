


const adobe = require('./AdobeEmployes.json')
const amazon = require('./AmazonEmployes.json')
const apple = require('./AppleEmployes.json')
const facebook = require('./FacebookEmployes.json')
const google = require('./GoogleEmployes.json')
const ibm = require('./IbmEmployes.json')
const microsoft = require('./MicrosoftEmployes.json')
const nvidia = require('./NividiaEmployes')
const oracle = require('./OracleEmployes.json')
const saleforce = require('./SalesforceEmployes.json')
const tesla = require('./TeslaEmployes.json')
const twiteer = require('./TwitterEmployes.json')
const uber = require('./UberEmployes.json')


let names = []

twiteer.employes.forEach(person => {
    names.push(`{"term": {"full_name": "${person.full_name}"}},`)
});

console.log(names.join('\n'))