var stTime = 0
var endTime = 0
var timerStart

var min
var sec
var milisec

var startBtn = document.getElementById('testStartBtn')
var stopBtn = document.getElementById('testStopBtn')
var recordList = document.getElementById('testRecordList')

startBtn.addEventListener('click', function() {
        // RECORD
    if(this.innerText == 'RECORD' && milisec) {
        console.log(min, sec, milisec)
        var li = document.createElement('li')
        li.style.color = "black"
        li.innerText = min + ' : ' + sec + ' : ' + milisec
        if(! recordList.firstChild) {
            recordList.append(li)
        }
        else {
            recordList.insertBefore(li, recordList.firstChild)
        }
        return false
    }

    this.innerText = 'RECORD'

    if(!stTime) {
        stTime = Date.now() // 최초 START
    }
    else {
        stopBtn.innerText = 'STOP'
        stTime += (Date.now() - endTime) // RESTART
    }

    timerStart = setInterval(function() {
        var nowTime = new Date(Date.now() - stTime)

        min = addZero(nowTime.getMinutes())
        sec = addZero(nowTime.getSeconds())
        milisec = addZero(Math.floor(nowTime.getMilliseconds() / 10))

        document.getElementById('postTestMin').innerText = min
        document.getElementById('postTestSec').innerText = sec
        document.getElementById('postTestMilisec').innerText = milisec
        }, 1)
    })

stopBtn.addEventListener('click', function() {
    if(timerStart) {
        clearInterval(timerStart) // STOP

        if(this.innerText == 'STOP') {
            endTime = Date.now()
            this.innerText = 'RESET'
            startBtn.innerText = 'RESTART'
        }
        else { // RESET
            stTime = 0
            min = 0
            sec = 0
            milisec = 0

            document.getElementById('postTestMin').innerText = '00'
            document.getElementById('postTestSec').innerText = '00'
            document.getElementById('postTestMilisec').innerText = '00'

            startBtn.innerText = 'START'
            this.innerText = 'STOP'
            timerStart = null
            recordList.innerHTML = ''
        }
    }
})

function addZero(num) {
    return (num < 10 ? '0'+num : ''+num)
}