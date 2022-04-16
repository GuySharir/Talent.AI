


const adobe = require('./AdobeEmployees.json')
const amazon = require('./AmazonEmployees.json')
const apple = require('./AppleEmployees.json')
const facebook = require('./FacebookEmployees.json')
const google = require('./GoogleEmployees.json')
const ibm = require('./IbmEmployees.json')
const microsoft = require('./MicrosoftEmployees.json')
const nvidia = require('./NividiaEmployes')
const oracle = require('./OracleEmployees.json')
const saleforce = require('./SalesforceEmployees.json')
const tesla = require('./TeslaEmployees.json')
const twiteer = require('./TwitterEmployees.json')
const uber = require('./UberEmployees.json')


let names = []

twiteer.employes.forEach(person => {
    names.push(`{"term": {"full_name": "${person.full_name}"}},`)
});

console.log(names.join('\n'))