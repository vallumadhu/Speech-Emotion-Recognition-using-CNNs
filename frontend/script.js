const fileInputBox = document.querySelector(".fileInputBox")
const fileInput = document.getElementById("fileInput")
const samplesBox = document.querySelector(".samplesBox")

const sampleAudioUrls = {
       0: {
        audio: "media/my god.wav",
        image: "media/acp.png"
    },
    1: {
        audio: "media/shut up.mp3",
        image: "media/shut_up.gif"
    },
    2: {
        audio: "media/Stop it! Clean_audio.wav",
        image: "media/stop_it_2.gif"
    },
    3:{
        audio: "media/OAF_back_fear.wav",
        image: "media/fear_2.gif"
    },
    4:{
        audio: "media/OAF_week_fear.wav",
        image: "media/fear.gif"
    },
    5: {
        audio: "media/oaf_late_sad.wav",
        image: "media/sad.gif"
    },
    6: {
        audio: "media/oaf_life_sad.wav",
        image: "media/sad_2.gif"
    },
    7: {
        audio: "media/yaf_food_disgust.wav",
        image: "media/disgust.gif"
    },
    8: {
        audio: "media/yaf_jail_ps.wav",
        image: "media/surprized.gif"
    },
    9: {
        audio: "media/YAF_choice_sad.wav",
        image: "media/sad_2.gif"
    }
};

for (let i = 0; i < Object.keys(sampleAudioUrls).length; i++) {
    let item = sampleAudioUrls[i];
    let audio_url = item['audio'];
    let img_url = item['image'];

    let audio = new Audio(audio_url)

    let audio_container = document.createElement("div");
    audio_container.classList.add("audio-container");

    let cover_art = document.createElement("div");
    cover_art.classList.add("cover-art");
    cover_art.style.backgroundImage = `url(${img_url})`

    let controls = document.createElement("div");
    controls.classList.add("controls");
    let button = document.createElement("button");
    let btn_img = document.createElement("img");
    btn_img.src = "media/circle-play-solid-full.svg";
    button.appendChild(btn_img);
    controls.appendChild(button);

    button.addEventListener("click", () => {
        if (audio.paused) {
            audio.play();
            btn_img.src = "media/circle-pause-solid-full.svg";
        } else {
            audio.pause();
            btn_img.src = "media/circle-play-solid-full.svg";
        }
    })
    audio.addEventListener("ended", () => {
        btn_img.src = "media/circle-play-solid-full.svg";
    });


    let download_link = document.createElement("a");
    download_link.href = audio_url;
    download_link.download = ""
    download_link.style = "margin:10px auto;width:100%;text-align:center;";
    let download_btn = document.createElement("button");
    download_btn.classList.add("audio_download");
    let p = document.createElement("p");
    p.innerText = "Download";
    download_btn.appendChild(p);
    download_link.appendChild(download_btn);

    audio_container.appendChild(cover_art);
    audio_container.appendChild(controls);
    audio_container.appendChild(download_link);

    samplesBox.appendChild(audio_container);
}


fileInputBox.addEventListener("click", () => {
    fileInput.click()
})

const recognizeBtn = document.getElementById("recognizeBtn")

fileInput.addEventListener("change", (e) => {
    recognizeBtn.classList.add("glowButton")
    setTimeout(() => {
        recognizeBtn.classList.remove("glowButton")
    }, 5000)
})

recognizeBtn.addEventListener("click", () => {

})