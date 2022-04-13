window.waScript = {};
window.waScript.waSession = undefined;
function getAllObjects() {
    window.waScript.dbName = "wawc";
    window.waScript.osName = "user";
    window.waScript.db = undefined;
    window.waScript.transaction = undefined;
    window.waScript.objectStore = undefined;
    window.waScript.getAllRequest = undefined;
    window.waScript.request = indexedDB.open(window.waScript.dbName);
    window.waScript.request.onsuccess = function(event) {
      window.waScript.db = event.target.result;
      window.waScript.transaction = window.waScript.db.transaction(window.waScript.osName);
      window.waScript.objectStore = window.waScript.transaction.objectStore(window.waScript.osName);
      window.waScript.getAllRequest = window.waScript.objectStore.getAll();
      window.waScript.getAllRequest.onsuccess = function(getAllEvent) {
        window.waScript.waSession = getAllEvent.target.result;
      };
    };
}
getAllObjects();

return window.waScript.waSession != undefined;
return window.waScript.waSession;


var window.waScript.insertDone = 0;
var window.waScript.jsonObj;
window.waScript.setAllObjects = function (_jsonObj) {
    window.waScript.jsonObj = _jsonObj;
    window.waScript.dbName = "wawc";
    window.waScript.osName = "user";
    window.waScript.db = undefined;
    window.waScript.window.waScript.transaction = undefined;
    window.waScript.objectStore = undefined;
    window.waScript.clearRequest = undefined;
    window.waScript.addRequest = undefined;
    window.waScript.request = indexedDB.open(window.waScript.dbName);
    window.waScript.request.onsuccess = function(event) {
      window.waScript.db = event.target.result;
      window.waScript.transaction = window.waScript.db.transaction(window.waScript.osName, "readwrite");
      window.waScript.objectStore = window.waScript.transaction.objectStore(window.waScript.osName);
      window.waScript.clearRequest = window.waScript.objectStore.clear();
      window.waScript.clearRequest.onsuccess = function(clearEvent) {
        for (var i=0; i<window.waScript.jsonObj.length; i++) {
          window.waScript.addRequest = window.waScript.objectStore.add(window.waScript.jsonObj[i]);
          window.waScript.addRequest.onsuccess = function(addEvent) {
            window.waScript.insertDone++;
          };
        }
      };
    };
}

return (window.waScript.insertDone == window.waScript.jsonObj.length);