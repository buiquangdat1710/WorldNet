$(document).ready(function() {
    $('#post-form').submit(function(e) {
        e.preventDefault();

        let post_caption = $("#post-caption").val();
        let post_visibility = $("#visibility").val();
        let generated_image_url = ""; // Thêm biến này để lưu URL ảnh AI

        // Kiểm tra nếu người dùng đã chọn ảnh
        var fileInput = $('#post-thumbnail')[0];
        var file = fileInput ? fileInput.files[0] : null;
        if (generatedImageFile) {
            file = generatedImageFile; // Gán file AI vào biến file
        }
        console.log("Caption:", post_caption);
        console.log("Visibility:", post_visibility);
        console.log("File:", file);
        
        // Kiểm tra nếu file tồn tại trước khi lấy thuộc tính .name
        var fileName = file ? file.name : '';

        var formData = new FormData();
        formData.append('post-caption', post_caption);
        formData.append('visibility', post_visibility);

        
        
        // Chỉ thêm file nếu nó tồn tại
        if (file) {
            formData.append('post-thumbnail', file, fileName);
        }
        if (generated_image_url) {
            formData.append('generated-image-url', generated_image_url);
        }
        
  
      $.ajax({
        url: '/create_post/',
        type: 'POST',
        dataType: 'json',
        data: formData,
        processData: false,
        contentType: false,  
        success: function(res){
            console.log("Response:", res);

            let _html = '<div class="card lg:mx-0 uk-animation-slide-bottom-small mt-3 mb-3">\
            <div class="flex justify-between items-center lg:p-4 p-2.5">\
                <div class="flex flex-1 items-center space-x-4">\
                    <a href="#">\
                        <img src="' + res.post.profile_image +'" class="bg-gray-200 border border-white rounded-full w-10 h-10">\
                    </a>\
                    <div class="flex-1 font-semibold">\
                        <div class="flex items-center">\
                            <a href="#" class="text-base font-semibold hover:text-blue-600 transition-colors duration-200 capitalize">' + res.post.username +'</a>\
                            <span class="flex ml-2">\
                                <span class="bg-green-500 h-2 w-2 rounded-full animate-pulse"></span>\
                                <span class="absolute inline-flex h-2 w-2 rounded-full bg-green-400 opacity-75 animate-ping"></span>\
                            </span>\
                        </div>\
                        <div class="flex items-center space-x-3 text-sm text-gray-500">\
                            <span class="inline-flex items-center">\
                                <span class="bg-gray-300 rounded-full h-1.5 w-1.5"></span>\
                            </span>\
                            <span class="inline-flex items-center group">\
                                <i class="far fa-clock text-blue-500 group-hover:text-blue-600 mr-1.5 transition-colors duration-200"></i>\
                                <span class="group-hover:text-gray-700 transition-colors duration-200">' + res.post.date +' ago</span>\
                            </span>\
                        </div>\
                    </div>\
                </div>\
                <div>\
                    <a href="#"> <i class="icon-feather-more-horizontal text-2xl hover:bg-gray-200 rounded-full p-2 transition -mr-1 dark:hover:bg-gray-700"></i> </a>\
                    <div class="bg-white w-56 shadow-md mx-auto p-2 mt-12 rounded-md text-gray-500 hidden text-base border border-gray-100 dark:bg-gray-900 dark:text-gray-100 dark:border-gray-700" uk-drop="mode: click;pos: bottom-right;animation: uk-animation-slide-bottom-small">\
                        <ul class="space-y-1">\
                            <li>\
                                <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
                            <i class="uil-share-alt mr-1"></i> Share\
                            </a>\
                            </li>\
                            <li>\
                                <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
                            <i class="uil-edit-alt mr-1"></i>  Edit Post \
                            </a>\
                            </li>\
                            <li>\
                                <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
                            <i class="uil-comment-slash mr-1"></i>   Disable comments\
                            </a>\
                            </li>\
                            <li>\
                                <a href="#" class="flex items-center px-3 py-2 hover:bg-gray-200 hover:text-gray-800 rounded-md dark:hover:bg-gray-800">\
                            <i class="uil-favorite mr-1"></i>  Add favorites \
                            </a>\
                            </li>\
                            <li>\
                                <hr class="-mx-2 my-2 dark:border-gray-800">\
                            </li>\
                            <li>\
                                <a href="#" class="flex items-center px-3 py-2 text-red-500 hover:bg-red-100 hover:text-red-500 rounded-md dark:hover:bg-red-600">\
                            <i class="uil-trash-alt mr-1"></i>  Delete\
                            </a>\
                            </li>\
                        </ul>\
                    </div>\
                </div>\
            </div>\
            '
            if(res.post.title){
                _html += '<div class="p-5 pt-0 border-b dark:border-gray-700 pb-3">\
                    ' + res.post.title +'\
                </div>\
                '
            }
            if(res.post.image){
                _html += '<div uk-lightbox>\
                    <a href= "' + res.post.image + '">\
                        <div class="aspect-auto"> <!-- Thêm container với aspect-ratio -->\
                            <img src="' + res.post.image + '" alt="" class="w-full h-full object-contain">\
                        </div>\
                    </a>\
                </div>\
                '
            }
            _html += '<div class="p-4 space-y-3">\
        <div class="flex space-x-4 lg:font-bold">\
            <a style = "cursor: pointer;" class="flex items-center space-x-2">\
                <div class="p-2 rounded-full like-btn' + res.post.id +' {% if request.user in p.likes.all %}text-blue-500 {% else %} text-black {% endif %} " id="like-btn" data-like-btn="' + res.post.id +'">\
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-blue-100">\
                        <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />\
                    </svg>\
                </div>\
                <div> Like</div>\
            </a>\
            <a href="#" class="flex items-center space-x-2">\
                <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                        <path fill-rule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clip-rule="evenodd" />\
                    </svg>\
                </div>\
                <div> <span id = "comment-count' + res.post.id +'">0</span> Comment</div>\
            </a>\
            <a href="#" class="flex items-center space-x-2 flex-1 justify-end">\
                <div class="p-2 rounded-full  text-black lg:bg-gray-100 dark:bg-gray-600">\
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="22" height="22" class="dark:text-gray-100">\
                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />\
                    </svg>\
                </div>\
                <div> Share</div>\
            </a>\
        </div>\
        <div class="flex items-center space-x-3 pt-2">\
            <div class="dark:text-gray-100">\
                <strong><span id="like-count' + res.post.id +'">0</span></strong> Like\
            </div>\
        </div>\
        <div class="border-t py-4 space-y-4 dark:border-gray-600" id = "comment-div' + res.post.id +'">\
        </div>\
        <div class="bg-gray-100 rounded-full relative dark:bg-gray-800 border-t">\
            <input placeholder="Add your Comment..." id="comment-input' + res.post.id +'" data-comment-input="' + res.post.id +'" class="bg-transparent max-h-10 shadow-none px-5 comment-input' + res.post.id +'">\
            <div class="-m-0.5 absolute bottom-0 flex items-center right-3 text-xl">          \
                <a style = "cursor: pointer;" id = "comment-btn" class = "comment-btn' + res.post.id +'" data-comment-btn="' + res.post.id +'">\
                    <ion-icon name="send-outline" class="hover:bg-gray-200 p-1.5 rounded-full"></ion-icon>\
                </a>\
            </div>\
        </div>\
    </div>\
        </div>\
        '     
            $("#create-post-modal").removeClass("uk-flex uk-open")
            $(".post-div").prepend(_html)   
        }
      });
    });
      // like post
    $(document).on("click", "#like-btn", function(){
        let btn_val = $(this).attr("data-like-btn")
        console.log(btn_val);
    
        $.ajax({
            url: "/like-post/",
            dataType: "json",
            data:{
                "id":btn_val
            },
            success: function(response){
                if (response.data.bool === true) {
                    console.log("Liked");
                    console.log(response.data.likes);
                    $("#like-count"+btn_val).text(response.data.likes)
                    $(".like-btn"+btn_val).addClass("text-blue-500")
                    $(".like-btn"+btn_val).removeClass("text-black")
                }else {
                    console.log("Unliked");
                    console.log(response.data.likes);
                    $("#like-count"+btn_val).text(response.data.likes)
                    $("#like-count"+btn_val).text(response.data.likes)
                    $(".like-btn"+btn_val).addClass("text-black")
                    $(".like-btn"+btn_val).removeClass("text-blue-500")
    
                }
                console.log(response.data.bool);
            }
        })
    })


    // Comment On Post
    $(document).on("click", "#comment-btn", function(){
        let id = $(this).attr("data-comment-btn")
        let comment = $("#comment-input"+id).val()
    
        console.log(id);
        console.log(comment);
    
        $.ajax({
            url: "/comment-post/",
            dataType: "json",
            data:{
                "id":id,
                "comment":comment,
            },
            success: function(response){
    
                let newComment = '<div class="flex card shadow p-2">\
                <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                    <img src="'+ response.data.profile_image +'" alt="" class="absolute h-full rounded-full w-full">\
                </div>\
                <div class="ml-3">\
                    <a href="#" class="text-base font-semibold hover:text-blue-600 transition-colors duration-200 capitalize">'+ response.data.username +'</a>\
                    <div class="text-gray-700 py-2 px-3 rounded-md bg-gray-100 relative lg:ml-5 ml-2 lg:mr-12  dark:bg-gray-800 dark:text-gray-100 flex items-center">\
                        <p class="leading-6"> '+ response.data.comment +'\
                        </p>\
                        <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                    </div>\
                    <div class="text-sm flex items-center space-x-3 mt-2 ml-5">\
                        <a id="like-comment-btn" data-like-comment="'+ response.data.comment_id +'"  class="like-comment'+ response.data.comment_id +'"  style="color: gray; cursor: pointer;" > <i class="fas fa-heart"></i>  </a> <small><span id="comment-likes-count'+ response.data.comment_id +'">0</span></small>\
                        <details >\
                            <summary>\
                            <div class="">Reply</div>\
                            </summary>\
                            <details-menu role="menu" class="origin-topf-right relative right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">\
                            <div class="pyf-1" role="none">\
                                <div class="p-1 d-flex" >\
                                    <input type="text"  class="with-border" name="" id="reply-input'+ response.data.comment_id +'">\
                                    <button id = "reply-comment-btn" data-reply-comment-btn="'+ response.data.comment_id +'" type="submit" class="block w-fulfl text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 reply-comment-btn'+ response.data.comment_id +'" role="menuitem">\
                                        <ion-icon name="send"></ion-icon>\
                                    </button>\
                                </div>\
                            </div>\
                            </details-menu>\
                        </details>\
                        <span> <small>'+ response.data.date +' ago</small> </span>\
                    </div>\
                    <div class = "reply-div'+ response.data.comment_id +'"></div>\
                </div>\
            </div>\
            '
                $("#comment-div"+id).prepend(newComment);
                $("#comment-count"+id).text(res.data.comment_count);
                $("#comment-input"+id).val("")
                
                console.log(response.data.bool);
            }
        })
    })

    //   LIke Comment
    $(document).on("click", "#like-comment-btn", function(){
        let id = $(this).attr("data-like-comment")
        console.log(id);

        $.ajax({
            url: "/like-comment/",
            dataType: "json",
            data:{
                "id":id
            },
            success: function(response){
                console.log(response.data.bool);
                console.log(response.data.likes);

                if (response.data.bool === true) {

                    $("#comment-likes-count"+id).text(response.data.likes)
                    $(".like-comment"+id).css("color", "red")

                }else {
                    console.log("Unliked");
                    console.log(response.data.likes);
                    $("#comment-likes-count"+id).text(response.data.likes)
                    $('#comment-icon'+id).removeClass(' text-red-600 ');
                    console.log($('.comment-icon'+id));
                    $("#comment-likes-count"+id).removeClass(' text-red-600 ');
                    $(".like-comment"+id).css("color", "gray")


                }
            }
        })
    })

    // Reply Comment
    $(document).on("click", "#reply-comment-btn", function(){
        let id = $(this).attr("data-reply-comment-btn")
        let reply = $("#reply-input"+id).val()

        console.log(id);
        console.log(reply);

        $.ajax({
            url: "/reply-comment/",
            dataType: "json",
            data:{
                "id":id,
                "reply":reply,
            },
            success: function(res){

                let newReply = ' <div class="flex mr-12 mb-2 mt-2" style="margin-right: 20px;">\
                    <div class="w-10 h-10 rounded-full relative flex-shrink-0">\
                        <img src="'+ res.data.profile_image +'" alt="" class="absolute h-full rounded-full w-full">\
                    </div>\
                    <div class="ml-2"> <!-- Thêm margin-left để tạo khoảng cách -->\
                        <a href="#" class="text-base font-semibold hover:text-blue-600 transition-colors duration-200 capitalize">'+ res.data.username +'</a>\
                        <div class="text-gray-700 py-1 px-3 rounded-md bg-gray-100 relative lg:ml-5 lg:mr-12 dark:bg-gray-800 dark:text-gray-100">\
                            <p class="leading-6">'+ res.data.reply +'</p>\
                            <div class="absolute w-3 h-3 top-3 -left-1 bg-gray-100 transform rotate-45 dark:bg-gray-800"></div>\
                        </div>\
                        <span> <small>'+ res.data.date +' ago</small> </span>\
                    </div>\
                </div>\
                '
                $(".reply-div"+id).prepend(newReply);
                $("#reply-input"+id).val("")
                
                console.log(res.data.bool);
            }
        })
    })

    // Delete Comment
    $(document).on("click", "#delete-comment", function(){
        let id = $(this).attr("data-delete-comment")
        console.log(id);

        $.ajax({
            url: "/delete-comment/",
            dataType: "json",
            data:{
                "id":id
            },
            success: function(request){
                console.log(request.data.bool);
                $("#comment-div"+id).addClass("d-none")
            }
        })
    })
    // Delete  Post
    $(document).on("click", ".delete-post-btn", function() {
        let postId = $(this).data("post-id"); // Lấy ID bài viết từ thuộc tính data
        $.ajax({
            url: "/delete-post/",
            type: "POST",
            data: {
                id: postId,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val() // Thêm CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // Xóa bài viết khỏi DOM
                    $("#post-" + postId).remove(); // Giả sử mỗi bài viết có id là post-<post_id>
                }
            },
            error: function(xhr, status, error) {
                console.error("Error deleting post:", error);
            }
        });
    });

    // Add Friend
    $(document).on("click", "#add-friend", function(){
        let id = $(this).attr("data-friend-id")
        console.log(id);

        $.ajax({
            url: "/add-friend/",
            dataType: "json",
            data:{
                "id":id
            },
            success: function(response){
                console.log("Bool ==",response.bool);
                if (response.bool == true) {
                    $("#friend-text").html("<i class='fas fa-user-minus'></i> Cancel Request ")
                    $(".add-friend"+id).addClass("bg-red-600")
                    $(".add-friend"+id).removeClass("bg-blue-600")
                }
                if (response.bool == false) {
                    $("#friend-text").html("<i class='fas fa-user-plus'></i> Add Friend ")
                    $(".add-friend"+id).addClass("bg-blue-600")
                    $(".add-friend"+id).removeClass("bg-red-600")
                }
            }
        })
    })

    // Accept Friend Request
    $(document).on("click", "#accept-friend-request", function(){
        let id = $(this).attr("data-request-id")
        console.log(id);

        $.ajax({
            url: "/accept-friend-request/",
            dataType: "json",
            data: {
                "id":id
            },
            success: function(response){
                console.log(response.data);
                $(".reject-friend-request-hide"+id).hide()
                $(".accept-friend-request"+id).html("<i class='fas fa-check-circle'></i> Friend Request Accepted")
                $(".accept-friend-request"+id).addClass("text-white")
            }
        })
    })


    // Reject Friend Request
    $(document).on("click", "#reject-friend-request", function(){
        let id = $(this).attr("data-request-id")
        console.log(id);

        $.ajax({
            url: "/reject-friend-request/",
            dataType: "json",
            data: {
                "id":id
            },
            success: function(response){
                console.log(response.data);
                $(".accept-friend-request-hide"+id).hide()
                $(".reject-friend-request"+id).html("<i class='fas fa-check-circle'></i> Friend Request Rejected")
                $(".reject-friend-request"+id).addClass("text-white")
            }
        })
    })

    // UnFriend User


    $(document).on("click", "#unfriend", function(){
        let id = $(this).attr("data-unfriend")
        console.log(id);
    
        $.ajax({
            url: "/unfriend/",
            dataType: "json",
            data: {
                "id":id
            },
            success: function(response){
                console.log(response);
                $("#unfriend-text").html("<i class='fas fa-check-circle'></i> Friend Removed ")
                $(".unfriend"+id).addClass("bg-green-600")
                $(".unfriend"+id).removeClass("bg-red-600")
            }
        })
    })
    
    
    $(document).on("click", "#block-user-btn", function(){
        let id = $(this).attr("data-block-user")
        
        $.ajax({
            url: "/block-user/",
            dataType: "json",
            data: {
                "id":id
            },
            success: function(response){
                console.log(response);
                $(".block-text"+id).html("<i class='fas fa-check-circle'></i> User Blocked Successfully. ")
            }
        })
    })
    

    $(document).on("click", "#block-user-btn", function(){
        let id = $(this).attr("data-block-user")
        
        $.ajax({
            url: "/block-user/",
            dataType: "json",
            data: {
                "id":id
            },
            success: function(response){
                console.log(response);
                $(".block-text"+id).html("<i class='fas fa-check-circle'></i> User Blocked Successfully. ")
            }
        })
    })

    
  });




