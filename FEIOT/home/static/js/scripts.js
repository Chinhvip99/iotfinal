const chart = new Chart("chartInformation", {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Temperature",
          borderColor: "red",
          backgroundColor: "red",
          lineTension: 0,
          data: [],
          fill: false,
        },
        {
          label: "Humidity",
          borderColor: "blue",
          backgroundColor: "blue",
          lineTension: 0,
          data: [],
          fill: false,
        },
        {
          label: "Light",
          borderColor: "orange",
          backgroundColor: "orange",
          lineTension: 0,
          data: [],
          fill: false,
        },
      ],
    },
    options: {
      onClick: function (event, elements) {
        if (elements.length > 0) {
          const datasetIndex = elements[0].datasetIndex;
          const meta = chart.getDatasetMeta(datasetIndex);
  
          meta.hidden = !meta.hidden;
  
          chart.update();
        }
      },
  
      scales: {
        x: {
          title: {
            display: true,
            text: "Time",
          },
        },
      },
  
      // onHover(event) {
      //   event.target.style.cursor = "default";
      // },
  
      // hover: {
      //     onHover: (event) => {
      //     event.target.style.cursor  = 'pointer';
      // }
      // },
    },
  });

var statusFan=0;
var statusLight=0;
var idFinal=0;
function updateChart() {
  const cartUrl = `http://127.0.0.1:8000/getHLTFinal`;
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
          if(responseData['id']!=idFinal){
            idFinal=responseData['id']
            const temp = responseData['temp'];
            const humid = responseData['hum'];
            const light = responseData['light'];
        
            if (chart.data.labels.length > 10) {
                chart.data.datasets.forEach(dataset => {
                    dataset.data.shift();
                });
                chart.data.labels.shift();
            }
        
            chart.data.datasets[0].data.push(temp);
            chart.data.datasets[1].data.push(humid);
            chart.data.datasets[2].data.push(light);
            chart.data.labels.push(responseData['time_created'].substring(11,19));
        
            let temperatureValueElement=document.getElementById("temperatureValue");
            const roundedTemp = Math.round(temp);
            temperatureValueElement.innerText = roundedTemp;
            if(temp < 25) {
              temperatureValueElement.parentNode.parentNode.style.background = "#FF3333";
            } else if(temp <= 31) {
                temperatureValueElement.parentNode.parentNode.style.background = "#FF0033";
            } else {
                temperatureValueElement.parentNode.parentNode.style.background = "#CC0033";
            }
            let humdValueElement=document.getElementById("humidityValue");
            humdValueElement.innerText = humid;
            if(humid < 50) {
              humdValueElement.parentNode.parentNode.style.background = "#E0FFFF";
            } else if(humid <= 60) {
                humdValueElement.parentNode.parentNode.style.background = "#00FFFF";
            } else {
                humdValueElement.parentNode.parentNode.style.background = "#00CED";
            }
            let lightValueElement=document.getElementById("lightValue");
            lightValueElement.innerText = light;
            // console.log(light/10)
            if(light < 600) {
              lightValueElement.parentNode.style.background = "#FFCC66";
            } else if(light <= 900) {
                lightValueElement.parentNode.style.background = "#FFCC33";
            } else {
                lightValueElement.parentNode.style.background = "#FFFF00";
            }
            
        
            chart.update();
          }
         
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
setInterval(updateChart, 2000);
function getStatusDevice(device){
  const cartUrl = `http://127.0.0.1:8000/getStatusDeviceFinal?device=${device}`;
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
          if(device=='led'){
            responseData['value']=="off"?statusLight=0:statusLight=1;
            if(responseData['value']=="off"){
                document.getElementById('light-img').src="/static/img/ledoff.png";
                document.getElementById('offLightImage').innerHTML="OFF";
            }else{
              document.getElementById('light-img').src="/static/img/ledon.gif";
              document.getElementById('offLightImage').innerHTML="ON";

            }
          }else{
            responseData['value']=="off"?statusFan=0:statusFan=1;

            if(responseData['value']=="off"){
              document.getElementById('fan-img').src="/static/img/fansnip.png";

              document.getElementById('offFanImage').innerHTML="OFF";
            }else{
            document.getElementById('fan-img').src="/static/img/fansnipgif.gif";

              document.getElementById('offFanImage').innerHTML="ON";
            }
          }
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
function setStatusDevicde(device){
  
  let cartUrl = `http://127.0.0.1:8000/device?device=${device}`;
  if(device=='fan'){
    statusFan==0?statusFan=1:statusFan=0;
    cartUrl+=`&status=${statusFan==0?"off":"on"}`;
    document.getElementById('offFanImage').innerHTML=`${statusFan==0?"OFF":"ON"}`;
    document.getElementById('offFanImage').style.background=`${statusFan==0?"red":"green"}`;

  }
  else if(device=='led'){
    statusLight==0?statusLight=1:statusLight=0;
    cartUrl+=`&status=${statusLight==0?"off":"on"}`;
    document.getElementById('offLightImage').innerHTML=`${statusLight==0?"OFF":"ON"}`;
    document.getElementById('offLightImage').style.background=`${statusLight==0?"red":"green"}`;


  }
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
          if(device=='led'){
            if(statusLight==0){
             
                document.getElementById('light-img').src="/static/img/ledoff.png";
                document.getElementById('light-img').style.background="red";
            }else{
              
              document.getElementById('light-img').src="/static/img/ledon.gif";
              document.getElementById('light-img').style.background="green";
              
            }
          }else{
            if(statusFan==0){
              
              document.getElementById('fan-img').src="/static/img/fansnip.png";
              document.getElementById('fan-img').style.background="red";
              
          }else{
           
            document.getElementById('fan-img').src="/static/img/fansnipgif.gif";
            document.getElementById('fan-img').style.background="green";


          }
          }
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
getStatusDevice('led');
getStatusDevice('fan');
