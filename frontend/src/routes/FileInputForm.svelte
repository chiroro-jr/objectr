<script lang="ts">
	import Button from './Button.svelte'

	export let videoAboveLimit = false
	export let files: FileList
	export let loading = false
</script>

<form class="py-10 gap-2 bg-gray-3" on:submit>
	<div class="flex flex-col gap-3 max-w-md mx-auto">
		<label for="video" class="text-blue font-semibold">Submit a video to detect objects</label>
		<!-- Add red outline or border if the video is above the limit
				Not uploaded
			-->
		<input
			type="file"
			accept="video/mp4, video/x-matroska"
			bind:files
			name="video"
			id="video"
			class="p-2 text-gray-4 text-sm bg-white rounded focus:outline-none focus:border-none file:outline-none file:border-none file:p-2 file:mr-3 file:bg-green file:text-white file:rounded file:hover:opacity-90 file:transition-all file:duration-200"
		/>
		{#if videoAboveLimit}
			<span class="text-xs text-red -mt-2">Video greater than 5MB. Upload another one.</span>
		{/if}
		<p class="text-sm text-gray-4">MP3, MKV (MAX: 5MB)</p>
		<Button type="submit" disabled={videoAboveLimit || !files || files?.length == 0 || loading}
			>Upload video</Button
		>
	</div>
</form>
