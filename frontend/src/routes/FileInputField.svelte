<script lang="ts">
	export let videoAboveLimit = false
	export let files: FileList
</script>

<div class="">
	<div class="flex flex-col gap-3">
		<label for="video" class="text-blue font-semibold">Submit a video to detect objects</label>
		<input
			type="file"
			accept="video/mp4, video/x-matroska"
			bind:files
			name="video"
			id="video"
			class="p-2 text-gray-4 text-sm bg-white rounded focus:outline-none focus:border-none file:outline-none file:border-none file:p-2 file:mr-3 file:bg-green file:text-white file:rounded file:hover:opacity-90 file:transition-all file:duration-200"
		/>
		{#if videoAboveLimit}
			<span class="text-xs text-red -mt-2">Video greater than 1MB. Upload a smaller one.</span>
		{/if}
		<p class="text-sm text-gray-4">MP4 (MAX: 1MB)</p>
	</div>
</div>
