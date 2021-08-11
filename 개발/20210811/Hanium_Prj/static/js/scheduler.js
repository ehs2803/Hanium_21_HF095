/* 변수 선언 */
var content = document.querySelector("#content"); // 폼의 텍스트 필드
var itemList = document.querySelector("#itemList"); // 웹 문서에서 부모 노드 가져오기
var items = document.querySelectorAll("li"); // 모든 항목 가져오기

/* 이벤트 핸들러 등록 */


/* 스케줄러 */
function Scheduler() {
    // 빈 항목이 존재할 경우
    if (content.value == "")
        return;

    // 내용이 있는 경우
    else {
        var newItem = document.createElement("li") // 리스트 추가
        newItem.className = 'lsclass';
        var newText = document.createTextNode(content.value); // 텍스트 필드의 값을 텍스트 노드로 만들기
        var newp_content = document.createElement("span");
        newp_content.appendChild(newText);
        newp_content.className = 'tempclass';
        var newButton = document.createElement("button"); // 요소 노드 추가
        var EndBtnText = document.createTextNode('할일 완료');
        newButton.appendChild(EndBtnText);
        newButton.className = 'button'
        newItem.appendChild(newp_content); // 텍스트 노드를 요소 노드의 자식 노드로 추가
        newItem.appendChild(newButton); // 할일 완료 버튼 추가
        itemList.insertBefore(newItem, itemList.childNodes[0]); // 자식 노드중 첫번째 노드 앞에 추가

        /* 삭제 */
        var items = document.querySelectorAll("li"); // 모든 항목 가져오기
        for (i = 0; i < items.length; i++) {
            // lastChild : newButton
            items[i].lastChild.addEventListener("click", function() {
                if (this.parentNode) // 부모 노드가 있다면
                    this.parentNode.remove(this); // 부모 노드에서 삭제
            });
        }
    }
}