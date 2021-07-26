function newRegister() {
  var newItem = document.createElement("li");  // 요소 노드 추가
  newItem.className='lsclass';

  var content = document.querySelector("#content");  // 폼의 텍스트 필드
  var newText = document.createTextNode(content.value);// 텍스트 필드의 값을 텍스트 노드로 만들기

  if(content.value=="") return;

  var newp_content = document.createElement("span");
  newp_content.appendChild(newText);
  newp_content.className = 'tempclass';

  var subjecttime=document.querySelector("#time");
  var newtime=document.createTextNode(subjecttime.value);
  if(subjecttime.value=="") return;
  var newp_time = document.createElement("span");
  newp_time.appendChild(newtime);
  newp_time.className = 'tempclass';

  var newButton = document.createElement("button");  // 요소 노드 추가
  var jbBtnText = document.createTextNode( '할일 완료' );
  newButton.appendChild(jbBtnText);

  newItem.appendChild(newp_content);  // 텍스트 노드를 요소 노드의 자식 노드로 추가
  newItem.appendChild(newp_time);  // 텍스트 노드를 요소 노드의 자식 노드로 추가
  newItem.appendChild(newButton);

  var itemList = document.querySelector("#itemList");  // 웹 문서에서 부모 노드 가져오기

  itemList.insertBefore(newItem, itemList.childNodes[0]);  // 자식 노드중 첫번째 노드 앞에 추가

  var items = document.querySelectorAll("li");  // 모든 항목 가져오기
  for(i=0; i<items.length; i++) {
    items[i].lastChild.addEventListener("click", function() {  // 항목 클릭했을 때 실행할 함수
      if(this.parentNode)    // 부모 노드가 있다면
        this.parentNode.remove(this);  // 부모 노드에서 삭제
    });
  }
}