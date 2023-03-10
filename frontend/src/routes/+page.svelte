<script lang="ts">
	import '../app.css'
	import Footer from './Footer.svelte'
	import Button from './Button.svelte'
	import FileInputForm from './FileInputForm.svelte'
	import Gradient from './Gradient.svelte'
	import NavBar from './NavBar.svelte'
	import { API_BASE_URL, toMB } from '../utils'

	let files: FileList
	let searchQuery = ''
	let videoAboveLimit = false
	let error: string | null = null
	let imageUrl = ''
	$: {
		if (files && files.length > 0) {
			videoAboveLimit = toMB(files[0].size) > 7
		}
	}

	let loading = false
	const uploadVideo = async (event: SubmitEvent) => {
		event.preventDefault()
		loading = true

		const video = files[0]
		const formData = new FormData()

		formData.append('query', searchQuery)
		formData.append('file', video)
		const res = await fetch(`${API_BASE_URL}/detect`, {
			method: 'POST',
			body: formData
		})

		loading = false

		// Object not found
		if (res.status === 404) {
			error = res.statusText
			return
		}

		// internal server error
		if (res.status >= 500) {
			error = res.statusText
			return
		}

		const blob = await res.blob()
		imageUrl = URL.createObjectURL(blob)
	}

	/*
		- upload files from svelte backend
		- upload files from svelte frontend
		- compared loadtimes
		- replace video placeholder with loader when submitting
		- replace loader with <video> when the response is received
		- replace video with query when user submits a filter for a specific object and then replace that with the actual video containing the detected object.
		- Add form validations on the frontend and backend
		- Store the submitted video somewhere to resubmit in case of a query
	*/
</script>

<div class="app-grid | w-full h-full">
	<Gradient />
	<NavBar />
	<!-- Video form -->
	<FileInputForm {videoAboveLimit} bind:files on:submit={uploadVideo} {loading} />
	<!-- Video Video-->
	<main class="bg-gray-2">
		<div class="main-grid | max-w-container mx-auto py-6 h-full">
			<!-- Object filter -->
			<div class="px-8  border-r-2 border-r-gray-3 ">
				<form class="flex flex-col gap-3">
					<label for="filter" class="whitespace-nowrap text-gray-4"
						>What are object are you looking for?</label
					>
					<input
						type="text"
						name="filter"
						id="filter"
						bind:value={searchQuery}
						class="p-3 rounded text-gray-4 focus:border-none focus:outline-blue/60 outline-offset-3 transition-all duration-200"
					/>
					<Button type="submit">Find object</Button>
				</form>
			</div>

			<!-- Video player -->
			<div class="flex flex-col gap-3 px-8">
				<h2 class="text-lg text-gray-4">Showing image of object in video</h2>
				<!-- player goes here -->
				{#if loading}
					<div class="flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center">
						Detecting Object...<br />
						Just a moment
					</div>
				{:else if error !== null}
					<div class="flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center">
						{error}
					</div>
				{:else if imageUrl === ''}
					<!-- else content here -->
					<div class="flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center">
						Upload a video
					</div>
				{:else}
					<div class="aspect-video">
						<img src={imageUrl} alt="Delected object" />
					</div>
				{/if}
			</div>
		</div>
	</main>
	<Footer />
</div>
