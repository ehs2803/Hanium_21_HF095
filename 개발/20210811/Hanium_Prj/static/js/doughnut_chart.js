// 그래프의 label
labels = ['Red', 'Blue', 'Yellow']

// 그래프의 데이터
const data = {
    labels: labels,
    datasets: [{
        label: 'Number of drowsiness',
        data: [300, 50, 100], // 졸음 데이터
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
        ],
        hoverOffset: 4
    }]
};

// 차트 설정
const d_config = {
    type: 'doughnut',
    data: data,
};

// 차트 객체 생성
var dChart = new Chart(
    document.getElementById('dChart'),
    d_config
);