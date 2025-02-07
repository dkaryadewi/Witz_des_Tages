window.onload = (event) => {
    set_video();
  };

function set_video() { 
    
    let final_video_name = `./final_video.mp4`
    
    let source = document.createElement("source");
    source.setAttribute("src", final_video_name);
    source.setAttribute("type", "video/mp4");

    document.getElementById("final_video").appendChild(source);
    
}