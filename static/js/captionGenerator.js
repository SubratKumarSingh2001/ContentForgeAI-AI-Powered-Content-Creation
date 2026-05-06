//JS-AJAX handling the status and showing different messages without rendering whole page
const status_area = document.getElementById("status-area");

//in case if status_area is not null then only start the polling and only end the polling if the status is completed or failed
if (status_area) {
  const caption_id = status_area.dataset.id;

  const interval = setInterval(() => {
    fetch(`/caption-status/${caption_id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "processing") {
          status_area.innerHTML = `
                    <div class="mt-8 border-2 border-dashed border-gray-300 rounded-xl p-10 sm:p-16 text-center bg-white">
                        <div class="flex flex-col items-center gap-4">
                            <div class="w-12 h-12 border-4 border-purple-300 border-t-purple-600 rounded-full animate-spin"></div>
                            <p class="text-gray-600 font-medium">Processing...🚀</p>
                        </div>
                    </div>`;
        } else if (data.status === "generating output") {
          status_area.innerHTML = `
                    <div class="mt-8 border-2 border-dashed border-gray-300 rounded-xl p-10 sm:p-16 text-center bg-white">
                        <div class="flex flex-col items-center gap-4">
                            <div class="w-12 h-12 border-4 border-yellow-300 border-t-yellow-600 rounded-full animate-spin"></div>
                            <p class="text-gray-600 font-medium">Generating Output...⌛</p>
                        </div>
                    </div>`;
        } else if (data.status === "completed") {
          status_area.innerHTML = `
                    <div class="mt-12 bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
                        <!-- Top Bar -->
                        <div class="flex items-center justify-between px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-b">
                            <div>
                                <h2 class="text-xl font-semibold text-gray-800">Your Generated Captions</h2>
                            </div>
                        </div>

                        <!-- Captions Content -->
                        <div class="p-8">
                            <article class="not-prose">
                                <!-- map is method of an array whereas in python it is separate function and both apply function to iterables i.e in js array.map() where map is method of array
                                     and apply method to each element of an array caption => means function(caption) { 'html apply to each element' } and this create the separate array and .join
                                     convert the new array into the separate HTML string -->
                                ${data.response.map(caption => `
                                    <div class="mb-4 p-4 bg-gray-100 rounded-lg">
                                        ${caption}
                                    </div>
                                `).join("")}
                            </article>
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
