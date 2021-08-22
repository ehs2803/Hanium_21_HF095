labels1 = [];
for (var key in dictObject_d) {
    labels1.push(key);
}
data_d = [];
for (var key in dictObject_d) {
    data_d.push(dictObject_d[key]);
}

data = {
    labels: labels1,
    datasets: [{
        label: 'Number of drowsiness detections this week',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: data_d,
    }]
};
const config1 = {
    type: 'line',
    data,
    options: {}
};
var myChart = new Chart(
    document.getElementById('myChart'),
    config1
);

// 도넛 차트
label = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24'
]
backgroundColors = ['rgb(255, 0, 0)', 'rgb(255, 187, 0)', 'rgb(171, 242, 0)', 'rgb(0, 216, 255)',
    'rgb(0, 89, 255)', 'rgb(255, 9, 221)', 'rgb(242, 203, 97)', 'rgb(135, 229, 132)', 'rgb(105, 109, 255)',
    'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)',
    'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)',
    'rgb(5, 9, 132)', 'rgb(5, 9, 132)', 'rgb(5, 9, 132)'
]

var dictObject_d_h = {}
tempdate = '2021-08-01'
for (var i = 0; i < d_data_js.length; i++) {
    if (String(d_data_js[i].d_time).substr(0, 10) === tempdate) {
        if (String(d_data_js[i].d_time).substr(11, 2) in dictObject_d_h) {
            dictObject_d_h[String(d_data_js[i].d_time).substr(11, 2)] += 1;
        } else {
            dictObject_d_h[String(d_data_js[i].d_time).substr(11, 2)] = 1;
        }
    }
}

labels_temp = []
data_temp = []
background_temp = []

var i = 0;
if (tempdate in dictObject_d) {
    for (var key in dictObject_d_h) {
        labels_temp.push(key);
        data_temp.push(dictObject_d_h[key]);
        background_temp.push(backgroundColors[i]);
        i += 1;
    }
} else {
    labels_temp.push("데이터 없음");
    data_temp.push(1);
    background_temp.push('rgb(0,0,0)');
}

const data = {
    labels: labels_temp,
    datasets: [{
        label: 'My First Dataset',

        data: data_temp,

        backgroundColor: background_temp,
        hoverOffset: 4
    }]
};

const config = {
    type: 'doughnut',
    data: data,
};

var dChart = new Chart(
    document.getElementById('dChart'),
    config
);