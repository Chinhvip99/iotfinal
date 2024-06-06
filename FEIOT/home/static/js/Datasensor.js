var searchKey=null;
var searchBy='All';
var sortBy=null;
var statusSort='0';
var statusSortID='0';
var statusSortTemp='0';
var statusSortHum='0';
var statusSortLight='0';
var statusSortDate='0';
var offset=0;
var nowList=0;
function setMid(){
    let midElement=document.getElementById('mid');
    let midHtml='<li valuePage="1" class="active">1</li>';
    for(var i = 2;i<=100;i++)
    {
        midHtml+=`<li valuePage="${i}">${i}</li>`;
    }
    midElement.innerHTML=midHtml;
    let listLI = document.querySelectorAll("li[valuePage]");
    console.log(listLI)
    // Thêm sự kiện 'click' cho từng mục li
    listLI.forEach(element => {
        element.addEventListener("click",(e)=>{
            document.querySelector("li[valuePage].active").classList.remove("active");
            e.target.classList.add("active");
            offset=(parseInt(e.target.getAttribute("valuePage"))-1)*4;
            getDataSensor();
        })
    });
}
setMid();
function convertUTCtoVietnamTime(utcTimeString) {
    // Tạo một đối tượng Date từ chuỗi thời gian UTC
    const utcDate = new Date(utcTimeString);

    // Lấy offset của múi giờ Việt Nam (UTC+7)
    const vietnamOffset = 7 * 60; // phút

    // Chuyển đổi sang múi giờ Việt Nam
    const vietnamDate = new Date(utcDate.getTime() + (vietnamOffset + utcDate.getTimezoneOffset()) * 60000);

    // Định dạng thời gian theo định dạng mong muốn, ví dụ: 'YYYY-MM-DD HH:mm:ss'
    const year = vietnamDate.getFullYear();
    const month = String(vietnamDate.getMonth() + 1).padStart(2, '0');
    const day = String(vietnamDate.getDate()).padStart(2, '0');
    const hours = String(vietnamDate.getHours()).padStart(2, '0');
    const minutes = String(vietnamDate.getMinutes()).padStart(2, '0');
    const seconds = String(vietnamDate.getSeconds()).padStart(2, '0');

    const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

    return formattedDate;
}
function getDataSensor(){
    const cartUrl = `http://127.0.0.1:8000/getvalue?${sortBy==null?"":"sortBy="+sortBy}&statusSort=${statusSort}&${searchKey==null?"":"searchKey="+searchKey}&searchBy=${searchBy}&offset=${offset}`;
    const xhr = new XMLHttpRequest();

    // Thiết lập phương thức và URL
    xhr.open('get', cartUrl, true);

    // Thiết lập tiêu đề 'Content-Type' để chỉ ra dạng dữ liệu là JSON
    xhr.setRequestHeader('Content-Type', 'application/json');
    // Xử lý sự kiện khi nhận được phản hồi từ máy chủ
    xhr.onload = function() {
        if (xhr.status === 200) {
            const responseData = JSON.parse(xhr.responseText);
            console.log(responseData);
            let tableHtml=
                `<tr>
                    <th>ID</th>
                    <th onclick="sortButton('temp')">Nhiệt Độ</th>
                    <th onclick="sortButton('hum')" >Độ ẩm</th>
                    <th onclick="sortButton('light')" >Ánh Sáng</th>
                    <th onclick="sortButton('date')" >Thời Gian</th>
                </tr>`;
            let tableElement = document.getElementById('tableDataSensor');
            for(var i=0;i<responseData.length;i++)
            {
                const localTime = convertUTCtoVietnamTime(responseData[i]['time_created']);
                tableHtml+=`
                    <tr>
                        <td>${responseData[i]['id']}</td>
                        <td>${responseData[i]['temp']}&deg;C</td>
                        <td>${responseData[i]['hum']}%</td>
                        <td>${responseData[i]['light']} LUX</td>
                        <td>${localTime}</td>
                    </tr>`;
            }
            tableElement.innerHTML=tableHtml;
        }else if(xhr.status === 403) {

        }
        else {
           
        }
    };

    // Xử lý sự kiện khi có lỗi xảy ra trong quá trình gửi yêu cầu
    xhr.onerror = function() {
        console.log('Lỗi trong quá trình gửi yêu cầu');
    };
    xhr.send();
}
getDataSensor();
function searchButton(){
    searchKey=document.getElementById("valueSearch").value;
    searchBy=document.getElementById("selectOption").value;
    statusSort='0';
    statusSortTemp='0';
    statusSortHum='0';
    statusSortLight='0'
    statusSortDate='0';
    offset=0;
    getDataSensor();
}
function sortButton(vl){
    switch (vl){
        case 'temp':
            statusSortTemp=='0'?statusSortTemp='1':statusSortTemp='0';
            statusSort=statusSortTemp
        case 'hum':
            statusSortHum=='0'?statusSortHum='1':statusSortHum='0';
            statusSort=statusSortHum
        case 'light':
            statusSortLight=='0'?statusSortLight='1':statusSortLight='0';  
            statusSort=statusSortLight
        case 'date':
            statusSortDate=='0'?statusSortDate='1':statusSortDate='0';  
            statusSort=statusSortDate

    }
    sortBy=vl;
    getDataSensor();
}

function nextList(vl){
    if(vl=='next'){
        nowList+=1;
    }else{
        nowList-=1;
    }
    document.getElementById('mid').style.transform=`translateX(-${nowList*150}px)`;
    // console.log(nowList);
    if(nowList!=0)
    {
        document.getElementById('pre').style.display="block";
    }else{
        document.getElementById('pre').style.display="none";
    }
}