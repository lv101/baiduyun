window.onload = function(){

	var result = document.getElementsByClassName("result")[0];
	var keyword = document.getElementsByClassName("text")[0];
	var submit = document.getElementsByClassName("submit")[0];
	var top = document.getElementsByClassName("top")[0];
	var bottom = document.getElementsByClassName("bottom")[0];
	var count = 0;
	var leng = 0;
	var tabNum = 'none';
	var timer;
	var tim = new Array();
	var timer2;
	var tim2 = new Array();;
	
	submit.onclick = function(){
		
		count = 0;
		top.innerHTML = '<span>正在搜索，请稍候...</span>';
		result.innerHTML = '';
		bottom.innerHTML = '';
		tabNum = Math.round(Math.random()*100000000);
		
		$.ajax({
			url: "/research",
			timeout: 10000,
			type: "get",
			data: {"keyword": keyword.value,
				   "tabnum": tabNum},
			success: function(){
				
			},
			error: function(xhr, type, errorThrown){
				console.log("发送tabnum请求失败！");
			}
		})
		
		timer = setInterval(function(){
			console.log(tabNum, typeof(tabNum));
			console.log('timer '+timer);
			if(tabNum != "none"){
				console.log('tim '+tim+' | '+!(timer in tim));
				if(!(timer in tim)){
					tim.push(timer);
				}
				$.ajax({
					url: '/ajax',
					timeout: 10000,
					type: "get",
					data: {"tabnum": tabNum},
					success: function(datas){
						
						datas = eval(datas);
						
						leng = datas.length;
						
						for(var i=0;i<datas.length;i++){
							
							if(i>count-1){
								result.innerHTML += "<span>" + datas[i].slice(0, -1).join(' | ') + ' | <a href="' + datas[i][datas[i].length-1] + '" target="_blank">' + datas[i][datas[i].length-1] + "</a></span>" + '<br>';
							}
							
						}
						console.log("count "+count+' | datas.length '+datas.length+ ' | leng ' + leng);
						
						if(datas.length){
							count = datas.length;
							bottom.innerHTML = '<span>已搜索到 '+ count +' 条记录</span>';
						}
						console.log("2count "+count+' | 2datas.length '+datas.length+ ' | 2leng ' + leng);
					},
					error: function(xhr, type, errorThrown){
						console.log("发送ajax请求失败！");
					}
				})
			}
		}, 3000);
		
		timer2 = setInterval(function(){
			console.log('timer2 '+timer2+' | '+!(timer2 in tim2));
			
			if(!(timer2 in tim2)){
				tim2.push(timer2);
			}
			
			if(count==0){
				top.innerHTML = '<span>啊哦，没有找到你要的资源哦 \>_\<</span>';
			}
			
			if(count > leng || count === leng){
				console.log('tim2 '+tim2);
				for(var i=0;i<tim.length;i++){
					clearInterval(tim[i]);
				}
				for(var i=0;i<tim.length;i++){
					clearInterval(tim2[i]);
				}
				top.innerHTML = '<span>查找结束</span>';
				tim = [];
				tim2 = [];
				console.log('2tim '+tim);
				console.log('2tim2 '+tim2);
			}
		}, 60000)
	}
	
	// document.onmousemove = function(){
	// 	return false
	// }
	
	// result.onmousemove = function(){
	// 	return false
	// }
	
}