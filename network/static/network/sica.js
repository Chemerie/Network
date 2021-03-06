document.addEventListener("DOMContentLoaded", function(){

	//Create Follow/Unfollow submit button
	var follow_btn = document.createElement("input");
	follow_btn.type = "submit";
	follow_btn.id = "follow_btn";
	follow_btn.class = "btn btn-primary";
	const follow_btn_div = document.querySelector("#follow-btn-div");




	//GET the follow database
	fetch("follow")
  	.then(response => response.json())
  	.then(followas =>{
    	console.log(followas);


    	var num_following =0; //Count the number of people followed by the user
		var num_followed =0; //Count the number of people following the user
		var followd = document.querySelector("#dguy").innerHTML;// get id of the follower from the html
		var followin = document.getElementById("followi-guy").innerHTML;// get id o f the followed from the html
		var followin_h5 = document.querySelector("#num_following");//get the id of the number following
		var followd_h5 = document.querySelector("#num_followed");// get the is of the nomber followed
		var is_following = false; //follwong status
		var follow_id = 0;

		//scan through the follow table
    	followas.forEach(followa=>{		

			if (followa.following == followd){num_following++;}//if the post owner appears at the following column of the table,
				//increase the number of following by one.	
			if (followa.followed == followd){num_followed++;}//if the post owner appears at the followed column of the table,
				//increase the number of followed by one.

			if (followa.following === followin && followa.followed === followd){// if the user is followint the post owner
				is_following = true;//return tru for following and rturn the id on the table
				follow_id = followa.id;
			}
    	})

    	followin_h5.innerHTML = num_following;//send the number of following to the html
    	followd_h5.innerHTML = num_followed;//send the number of followed to the html

    	//if the user is not the post owner, append follow button
    	if (followd !== followin){
    		follow_btn_div.append(follow_btn);
    		if (is_following){
				follow_btn.value = "Unfollow";		
			} else if(!is_following){
				follow_btn.value = "Follow";
			}
    	}
    	//When the user clicks on the follow/ unfollow button
    	document.querySelector("#follow_form").onsubmit = ()=>{
    	//if it's follow button, add 1 to the number of followed, return true for following and change button value to Unfollow
		//equally send the following and followed to the database
		if (!is_following){

			followd_h5.innerHTML = parseInt(followd_h5.innerHTML) + 1;
			is_following = true;
			follow_btn.value = "Unfollow";

			fetch("/addfollow", {
				method: 'POST',
				body: JSON.stringify({
					following: followin,
					followed: followd
				})
			})
  			.then(response => response.json())
  			.then(followas =>{
  				console.log(follow_btn.name);

  		});
  		//if it's an Unfollow button, return false for isfollowing, change button value to Foloow
  		//equally delete the row of following and followed in the database
		}else if(is_following){
			followd_h5.innerHTML = parseInt(followd_h5.innerHTML) - 1;
			is_following = false;
			follow_btn.value = "Follow";

		fetch(`unfollow/${follow_id}`)
  		.then(response => response.json())
  		.then(followas =>{
  			console.log(follow_btn.name);
  		});
	}
	return false;
}  
})
  	//get the posts from the database
	fetch("getpost")
  	.then(response => response.json())
  	.then(posts =>{
  		//get nodelists of the various posts from the template
    	var content_edited = document.querySelectorAll(".content");//post contents div
    	var edit_bts = document.querySelectorAll(".edit-button");//edit buttons
    	var edit_btns = Array.prototype.slice.call(edit_bts);//edit buttons to array
    	var content_edits = document.querySelectorAll(".content-edit");//editable contents
    	var save_btns = document.querySelectorAll(".save-button");//the save buttons
    	var main_content = document.querySelectorAll(".main-content");// the main content
    	var edit_content = document.querySelectorAll(".edit-content");// the editable content
    	var post_ids =  document.querySelectorAll(".post-id");//post ids
    	//for every post that returs from the database
    	posts.forEach(post=>{
    	//for each edit button on the temperate
		edit_btns.forEach(button =>{
			var index = edit_btns.indexOf(button)//get the button index
			//clicking the button hides the main content, displays the editable content with the save button
			button.onclick = ()=>{
				content_edited[index].style.display = 'none';
				content_edits[index].style.display = 'block';
				edit_bts[index].style.visibility = 'hidden';
				//clicking on the save button, saves the edited content, displays the main content updated
				save_btns[index].onclick = ()=>{
					var content = edit_content[index].value;
					main_content[index].innerHTML = content;
					var id = post.id;
					console.log(post_ids[index].innerHTML)
					fetch(`post/${post_ids[index].innerHTML}`, {
          				method: "PUT",
          				body: JSON.stringify({
          				content: content
        					})
      				})
					content_edits[index].style.display = 'none';
					content_edited[index].style.display = 'block';
					edit_bts[index].style.visibility = 'visible';
				}
			}
			})

		})  		
	})

  			//get the Like features of each post from the template(nodelists)
			var like_counts =  document.querySelectorAll(".like-count");// the like counts
			var post_ids =  document.querySelectorAll(".post-id");//the post ids
	  		var like_bts =  document.querySelectorAll(".like-button");// the Like buttons
			var like_btns = Array.prototype.slice.call(like_bts);// the like buttons into array	
			var user = document.querySelector("#main-user");//the user

			var likepid=[];
			var liker=[];
			var likeid=[];
				//fetch the like table from the database
				fetch("like")
  				.then(response => response.json())
  				.then(likes =>{
  				//for each of the returned data, get the post id and the like id where the user is the like 
  				//and add to the post id(likepid) and like id(likeids) arrays 
    			likes.forEach(like=>{
    				if (like.liker == user.innerHTML){
    					likepid.push(like.p_id);
    					likeid.push(like.id);
    				}


    			})

    			var likepids= likepid.reverse();
				var likers=(liker.reverse());
				var likeids=(likeid.reverse());
				console.log(likepids, likers, likeids );


				like_btns.forEach(buttons=>{
					var indexa = like_btns.indexOf(buttons)
					like_bts[indexa].innerHTML = "Like";
					var liked_id = 0;

					num_counted = [];
					fetch("like")
  					.then(response => response.json())
  					.then(likes =>{
  						var num_like = 0;
  						likes.forEach(like=>{
  						if(like.p_id === (parseInt(post_ids[indexa].innerHTML ))){
  							num_like = num_like + 1;
  						}

	  				})
  						num_counted.push(num_like);


  					console.log(num_counted);
  					like_counts[indexa].innerHTML = num_counted[indexa];
					if (likepids.includes(parseInt(post_ids[indexa].innerHTML ))){
						like_bts[indexa].innerHTML = "Unlike";
						var d_id=0;
						likepids.forEach(liken=>{
							var inde = likepids.indexOf(liken);
							if (likepids[inde] == post_ids[indexa].innerHTML){
								d_id = likeids[inde];
								// console.log(d_id);
							}
							})
						like_bts[indexa].onclick = ()=>{
    						fetch(`deletelike/${d_id}`)
							.then(response => response.json())
							.then(posts => {
							like_bts[indexa].innerHTML = "Like";
							like_counts[indexa].innerHTML = parseInt(like_counts[indexa].innerHTML) - 1;
							});
							return false;
						}

					}else{
						like_bts[indexa].innerHTML = "Like";
						like_bts[indexa].onclick = ()=>{
    						fetch(`addlike/${parseInt(post_ids[indexa].innerHTML)}`)
							.then(response => response.json())
							.then(posts => {

						like_bts[indexa].innerHTML = "Unlike";
						like_counts[indexa].innerHTML = parseInt(like_counts[indexa].innerHTML) + 1;
							});
							return false;

    					}
					}
					})



					})



			})






});