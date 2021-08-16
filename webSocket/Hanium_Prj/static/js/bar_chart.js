// 그래프의 x 축 : 월화수목금토일
labels = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'];

// 그래프로 표시할 데이터
data = {
    labels: labels,
    datasets: [{
        label: 'Number of drowsiness detections this week',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 6, 2, 1, 4, 5, 8], // 일별 졸음데이터
    }]
};

// 그래프 설정
const bar_config = {
    type: 'line',
    data,
    options: {}
};

// 그래프 객체 생성
var bChart = new Chart(
    document.getElementById('bChart'),
    bar_config
);