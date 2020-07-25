
/* //백업 1
// 테스트 코드.
const sheetId = "1b3opsb5l7DeZRKKPJS6MlXh-Fu12ViXZz8tVlQ_lgR8";
const apiKey = "AIzaSyB28kcFVow6yy_mYgfbER-H0_wfuo4l6cg";
var requestURL  = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/?key=${apiKey}&includeGridData=true`;
function sendRequest(requestURL) {
    var request = new XMLHttpRequest();
    request.open("GET", requestURL, true);
    request.responseType = "json";
    request.send();
    return request.responseText;
}

// 꼭 참고해봐!
// https://gist.github.com/msmfsd/fca50ab095b795eb39739e8c4357a808 
async function fetchAsync (url) {
    let response = await fetch(url);
    let data = await response.json();
    return data;
  }

// fetchAsync(requestURL).then(data => console.log(data)).catch(reason => console.log(reason.message));
const data = fetchAsync(requestURL);
*/


let theUrl = "https://spreadsheets.google.com/feeds/list/1b3opsb5l7DeZRKKPJS6MlXh-Fu12ViXZz8tVlQ_lgR8/os9ojag/public/values?alt=json"

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

// 구글 스프레드 시트 데이터를 가져오면, 아직 스트링임.
const stringData = httpGet(theUrl);

const testMountains = JSON.parse(stringData);
let mountains = testMountains.feed.entry;


// API로 불러오는 데이터 중 필요 없는 컬럼 삭제
deleteKeys = ['id', 'updated', 'category', 'title', 'content', 'link', 'gsx$text'];
for (let element of mountains) {
    for (deleteKey of deleteKeys) {
        delete element[deleteKey];
    }
    // console.log(element);
}


function renameKeys(obj, newKeys) {
    const keyValues = Object.keys(obj).map(key => {
      const newKey = newKeys[key] || key;
      return { [newKey]: obj[key] };
    });
    return Object.assign({}, ...keyValues);
  }

const newKeys = { gsx$idx : "No."
                , gsx$price숫자 : "가격"
                , gsx$sitevarchar : "사이트"
                , gsx$title : "문서 제목"
                , gsx$inch : '사이즈'
                , gsx$volume : '용량'
                , gsx$wifi : '와이파이/셀룰러'
                , gsx$model : '모델'
                , gsx$generation : '세대'
                , gsx$date : '등록일'
                , gsx$link : '링크'};
for (let element of mountains) {
    for (key in newKeys) {
        let newKey = newKeys[key];
        element[newKey] = element[key];
        delete element[key];
    }
}
// const mountains = renameKeys(mountains, newKeys);


// ref. : https://www.valentinog.com/blog/html-table/
// let myMountains = [
//     { name: "Monte Falco", height: 1658, place: "Parco Foreste Casentinesi" },
//     { name: "Monte Falterona", height: 1654, place: "Parco Foreste Casentinesi" },
//     { name: "Poggio Scali", height: 1520, place: "Parco Foreste Casentinesi" },
//     { name: "Pratomagno", height: 1592, place: "Parco Foreste Casentinesi" },
//     { name: "Monte Amiata", height: 1738, place: "Siena" }
//   ];
  
  function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }
  
  function generateTable(table, data) {
    // 객체에서 key만 가져옴
    for (let element of data) {
      let row = table.insertRow();
      // 하나의 key들을 가져옴.
      for (key in element) {
        let cell = row.insertCell();
        let text = document.createTextNode(element[key].$t);
        cell.appendChild(text);
      }
    }
  }
  
let table = document.querySelector("table");
let data = Object.keys(mountains[0]); // 테이블 헤더로 쓸 키를 불러옴
generateTableHead(table, data); // 테이블 헤더 생성
generateTable(table, mountains);

// console.log(Object.keys(mountains[0]));
// for (let elements of mountains) {
//     for (let element in elements) {
//         console.log(elements[element].$t);
//     }
// }



/* 주석
                    <tr>
                        <th>No.</th>
                        <th>사이트</th>
                        <th>사이즈</th>
                        <th>용량</th>
                        <th>Wi-Fi/Cellular</th>
                        <th>가격</th>
                        <th>링크</th>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>중고나라</td>
                        <td>11"</td>
                        <td>64GB</td>
                        <td>Wi-Fi</td>
                        <td>100만원</td>
                        <td>http://rakkoon.co.kr</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>당근마켓</td>
                        <td>12.9"</td>
                        <td>512GB</td>
                        <td>Cellular</td>
                        <td>129만원</td>
                        <td>http://rakkoon.co.kr</td>
                    </tr>
*/






// API 호출 후 데이터를 불러옴(근데, 아직 각 로우 데이터를 못 가져옴.)
// fetch(requestURL).then(function(response) {
//     return response.json();
//   }).then(function(data) {
//     console.log(data);
//   }).catch(function() {
//     console.log("Booo");
//   });





// const sheetId = "1b3opsb5l7DeZRKKPJS6MlXh-Fu12ViXZz8tVlQ_lgR8";
// const apiKey = "AIzaSyB28kcFVow6yy_mYgfbER-H0_wfuo4l6cg";
// fetch('https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/?key=${apiKey}&includeGridData=true')
//   .then(function(response) {
//     return response.json();
//   })
//   .then(function(myJson) {
//     console.log(JSON.stringify(myJson));
//   });





// function tableCreate() {
//     var body = document.body,
//         tbl = document.createElement('table');
//     tbl.style.width = '100px';
//     tbl.style.border = '1px solid black';

//     for(var i = 0; i < 10; i++) {
//         var tr = tbl.insertRow();
//         for(var j = 0; j < 2; j++){
//             if(i == 2 && j == 1) {
//                 break;
//             } else {
//                 var td = tr.insertCell();
//                 td.appendChild(document.createTextNode('Cell'));
//                 td.style.border = '1px sold black';
//                 if(i == 1 && j == 1){
//                     td.setAttribute('rowSpan', '2');
//                 }
//             }
//         }
//     }
//     body.appendChild(tbl);
// }
// tableCreate();



// // function tableCreate(){
// //     var body = document.body,
// //         tbl  = document.createElement('table');
// //     tbl.style.width  = '100px';
// //     tbl.style.border = '1px solid black';

// //     for(var i = 0; i < 3; i++){
// //         var tr = tbl.insertRow();
// //         for(var j = 0; j < 2; j++){
// //             if(i == 2 && j == 1){
// //                 break;
// //             } else {
// //                 var td = tr.insertCell();
// //                 td.appendChild(document.createTextNode('Cell'));
// //                 td.style.border = '1px solid black';
// //                 if(i == 1 && j == 1){
// //                     td.setAttribute('rowSpan', '2');
// //                 }
// //             }
// //         }
// //     }
// //     body.appendChild(tbl);
// // }
// // tableCreate();