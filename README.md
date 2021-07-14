# Tumblr

Implemented Tumblr Blog using Strategy pattern

http://127.0.0.1:8000/posts/create   -> To create a post

http://127.0.0.1:8000/posts/all   -> To get all created posts

http://127.0.0.1:8000/posts/<1>  -> To get/update/delete a specific post (postid 1)

http://127.0.0.1:8000/posts/all?type=<blogtype> -> To get all posts of a blogtype (blogtypes -> blog,quote,bookmark,image,video,github)

http://127.0.0.1:8000/posts/<1>/files/all -> To get all files in a specific post (postid 1)

http://127.0.0.1:8000/posts/<1>/files/add -> To add files to a specific post (postid 1)

http://127.0.0.1:8000/posts/<1>/files/<1> -> To get a specific file in a specific post (postid 1, fileid 1)

-------------------------------------------------------------------------------------------------------------------------------------

Samples for each API:

1) To create a post

   POST Request: http://127.0.0.1:8000/posts/create
		
		{"user":"user1","post_type":"Blog","content_data":{"text1":"t1","text2":"t2"},"likes":1,"tags":"#user1"}
		{"user":"user2","post_type":"Quote","content_data":{"text1":"t1","text2":"t2"},"likes":1,"tags":"#user2"}
		{"user":"user3","post_type":"Video","content_data":{"url":"https://www.youtube.com/watch?v=fEE4RO-_jug&t=5s","caption":"F9 trailer 2"},"likes":1,"tags":"#user3"}
		{"user":"user4","post_type":"Image","content_data":{"url":"imageurl","caption":"imageurl"},"likes":1,"tags":"#user4"}

---------------------------------------------------------------------------------------------------------------------------------------

2) To get all created posts

Get Request -> http://127.0.0.1:8000/posts/all

Response -> 
	[{"id":7,"user":"user1","post_type":"Video","content_data":{"url":"https://www.youtube.com/watch?v=fEE4RO-_jug&t=5s","caption":"F9 trailer 2"},"likes":1,"tags":"#user1","files":[]},
	{"id":8,"user":"user1","post_type":"Blog","content_data":{"text1":"t1","text2":"t2"},"likes":1,"tags":"#user1","files":[]},
	{"id":9,"user":"user2","post_type":"Quote","content_data":{"text1":"t1","text2":"t2"},"likes":1,"tags":"#user2","files":[]},
	{"id":10,"user":"user3","post_type":"Video","content_data":{"url":"https://www.youtube.com/watch?v=fEE4RO-_jug&t=5s","caption":"F9 trailer 2"},"likes":1,"tags":"#user3","files":[]},
	{"id":11,"user":"user4","post_type":"Image","content_data":{"url":"imageurl","caption":"imageurl"},"likes":1,"tags":"#user4","files":[]}]

---------------------------------------------------------------------------------------------------------------------------------------

3) To update a post (to update likes to zero for post 7)

PUT Request:  http://127.0.0.1:8000/posts/7

		form data -> {"likes":0}

Response : {"id":7,"user":"user1","post_type":"video","content_data":{"url":"https://www.youtube.com/watch?v=fEE4RO-_jug&t=5s","caption":"F9 trailer 2"},"likes":0,"tags":"#user1","files":[]}

---------------------------------------------------------------------------------------------------------------------------------------

4) To get posts of all blogtype 'Quote'

Get Request : http://127.0.0.1:8000/posts/all?type='Quote'

Response : {"id":9,"user":"user2","post_type":"Quote","content_data":{"text1":"t1","text2":"t2"},"likes":1,"tags":"#user2","files":[]} 

---------------------------------------------------------------------------------------------------------------------------------------

5) To add files to a post (to add files to postid 1)

	POST Request: http://127.0.0.1:8000/posts/1/files/add
	
	Request Payload : {"files":["/path/to/file"]}

---------------------------------------------------------------------------------------------------------------------------------------

6) To get all files in a specific post (to get all files of post postid 1)

Get Request: http://127.0.0.1:8000/posts/1/files/all

Response : [{"id":1,"file":"/images/avengers_infinity_war_characters_4k_8k-768x1280.jpg","post":1},
		{"id":2,"file":"/images/avengers_infinity_war_characters_4k_8k-768x1280_ugwdxOo.jpg","post":1},
		{"id":3,"file":"/images/cars_3_2017_4k_8k-7680x4320_xn2CZFn.jpg","post":1}]



