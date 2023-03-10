<script lang="ts">
	import '../app.css'
	import Footer from './Footer.svelte'
	import Button from './Button.svelte'
	import FileInputForm from './FileInputField.svelte'
	import Gradient from './Gradient.svelte'
	import Logo from './Logo.svelte'
	import { API_BASE_URL, toMB } from '../utils'
	import { classNames } from './class_names'

	let files: FileList
	let searchQuery = ''
	let videoAboveLimit = false
	let error: string | null = null
	let imageUrl = ''
	$: {
		if (files && files.length > 0) {
			videoAboveLimit = toMB(files[0].size) > 1
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
</script>

<div class="app-grid | w-full h-full">
	<Gradient />
	<aside class="left | bg-gray-2 p-4 flex flex-col gap-4">
		<Logo />
		<FileInputForm {videoAboveLimit} bind:files />
		<div>
			<form class="flex flex-col gap-3" on:submit|preventDefault={uploadVideo}>
				<label for="query" class="whitespace-nowrap text-gray-4"
					>What are object are you looking for?</label
				>
				<input
					type="text"
					name="query"
					id="query"
					bind:value={searchQuery}
					class="p-3 rounded text-gray-4 focus:border-none focus:outline-blue/60 outline-offset-3 transition-all duration-200"
				/>
				<Button
					type="submit"
					disabled={videoAboveLimit || !files || files?.length == 0 || loading || searchQuery == ''}
					>Find object</Button
				>
			</form>
		</div>
		<div class="mt-auto text-sm text-gray-4 p-3 bg-gray-1 rounded-md space-y-3">
			<div>
				<h3 class="text-blue font-bold">Group Members</h3>
				<ul>
					<li>Nyasha Chiroro - R187470B</li>
					<li>Mc Samuel Shoko - R1810066</li>
					<li>Anesu Masora - R187496Q</li>
				</ul>
			</div>
			<div>
				<h3 class="text-blue font-bold">Reference Links</h3>
				<ul>
					<li>
						<a
							href="https://github.com/chiroro-jr/objectr"
							target="_blank"
							class="text-green underline">GitHub repository for project</a
						>
					</li>
				</ul>
			</div>
		</div>
	</aside>
	<main class="main">
		<div class=" flex flex-col gap-4 h-full">
			<h2 class="text-lg text-gray-4 text-center py-4">Search for objects in videos</h2>
			<!-- diclaimer -->
			<div class="px-28">
				<p class="text-sm text-gray-4 p-3 bg-gray-2 rounded-md">
					Due to memory limitations (512MB) on free options of deployment platforms such as <a
						class="text-green underline"
						href="https://render.com"
						target="_blank">Render</a
					>
					where we deployed, we could not deploy the full model nor allow larger videos. The server was
					simply running out of memory. However you can find the code for this application in
					<a
						href="https://github.com/chiroro-jr/objectr"
						target="_blank"
						class="text-green underline">this GitHub repository</a
					> with all the detection code commented out. Everything else works. A test video is available
					in the repository.
				</p>
			</div>

			<div class="px-28 pb-4 flex-1">
				{#if loading}
					<div class="flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center h-full">
						Detecting Objects...<br />
					</div>
				{:else if error !== null}
					<div class="flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center h-full">
						{error}
					</div>
				{:else if imageUrl === ''}
					<div class="flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center h-full">
						Upload a video
					</div>
				{:else}
					<div
						class="frame-container | flex-1 bg-gray-3 rounded text-gray-4 grid place-content-center max-h-[400px] overflow-y-scroll"
					>
						<img src={imageUrl} class="object-cover" alt="Delected object" />
					</div>
				{/if}
			</div>
		</div>
	</main>
	<aside class="right | max-w-full overflow-y-scroll p-4 bg-gray-2 flex flex-col gap-2">
		<h2 class="text-blue">Searchable objects</h2>
		<ul>
			{#each classNames as item}
				<li>{item}</li>
			{/each}
		</ul>
	</aside>
	<Footer />
</div>
