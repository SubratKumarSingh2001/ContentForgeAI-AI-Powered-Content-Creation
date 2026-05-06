//Multiple files taking as an input

let fileCounter = 2; //Start with 2 as we already have file1

function addFileInput() {
  const fileInput = document.getElementById("fileInputs");
  const newFileInput = document.createElement("div");
  newFileInput.className =
    "p-3 rounded-lg border border-purple-300 individual-input mt-2";
  newFileInput.innerHTML = `
        <div class="flex items-center justify-between gap-3">
            <input
                type="file"
                name="file${fileCounter}"
                class="font-poppins block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-purple-100 file:text-purple-700 hover:file:bg-purple-200"
            />

            <button
                class="w-8 h-8 flex items-center justify-center rounded-full bg-red-500 text-white hover:bg-red-600"
                type="button"
                onclick="removeFileInput(this)"
            >
                ✕
            </button>
        </div>

        <input
            type="number"
            id="durationInput"
            name="duration"
            placeholder="Duration (sec)"
            class="mt-3 w-full px-3 py-2 rounded-md border border-gray-400 text-sm focus:ring-2 focus:ring-purple-400"
        />
    `;
  fileInput.append(newFileInput);
  fileCounter++;
}

function removeFileInput(button) {
  const fileInputGroup = button.closest(".individual-input"); //it will find the closet ancestor with the given class name
  fileInputGroup.remove();
}

//JS-AJAX handling the status and showing different messages without rendering whole page
const status_area = document.getElementById("status-area");

//in case if status_area is not null then only start the polling and only end the polling if the status is completed or failed
if (status_area) {
  const rec_id = status_area.dataset.recId;

  const interval = setInterval(() => {
    fetch(`/reel-status/${rec_id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "uploading") {
          status_area.innerHTML = `
                    <div class="flex flex-col items-center gap-4">
                        <div class="w-12 h-12 border-4 border-purple-300 border-t-purple-600 rounded-full animate-spin"></div>
                        <p class="text-gray-600 font-medium">Uploading...🚀</p>
                    </div>`;
        } else if (data.status === "processing") {
          status_area.innerHTML = `
                    <div class="flex flex-col items-center gap-4">
                        <div class="w-12 h-12 border-4 border-yellow-300 border-t-yellow-600 rounded-full animate-spin"></div>
                        <p class="text-gray-600 font-medium">Processing your reel...⌛</p>
                    </div>`;
        } else if (data.status === "completed") {
          status_area.innerHTML = `
                    <div class="flex flex-col items-center gap-2 p-6">
                        <!-- Animated Tick -->
                        <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center animate-bounce">
                          <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                          </svg>
                        </div>

                        <!-- Text OUTSIDE card -->
                        <p class="text-gray-800 font-semibold text-xl">Completed... ✅</p>
                        <p class="text-gray-500 font-medium text-lg">Your Reel is Ready 🤩</p>

                        <!-- Reel ONLY -->
                        <div class="w-full max-w-md p-4 rounded-2xl shadow-xl bg-white flex flex-col items-center gap-4 mt-3">

                          <video controls controlsList="nodownload" class="h-90 rounded-xl shadow w-full">
                            <source src="${data.video}" type="video/mp4">
                          </video>

                          <!-- Download Button -->
                          <a href="${data.video}" download class="bg-gradient-to-r from-indigo-600 to-pink-400 hover:from-indigo-700 hover:to-pink-500 text-white px-6 py-3 
                            rounded-full shadow-lg transform hover:scale-105 active:scale-95 hover:shadow-2xl transition-all duration-300 ease-in-out">
                            Download Reel ⬇️ 
                          </a>
                        </div>
                    </div>`;
                    clearInterval(interval);
        } else if (data.status === "failed") {
          status_area.innerHTML = `
                    <div class="flex flex-col items-center gap-4">
                        <p class="text-gray-600 font-medium">Failed Something Went Wrong...❌</p>
                    </div>`;
                    clearInterval(interval);
        }
      });
  }, 3000);
}
