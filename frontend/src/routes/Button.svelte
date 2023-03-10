<script lang="ts">
	export let disabled: boolean = false
	export let type: 'submit' | 'button' | 'reset' = 'button'
</script>

<button
	{type}
	{disabled}
	class="bg-green text-white p-3 rounded hover:opacity-90 transition-all duration-200 disabled:bg-gray-4/60 disabled:text-gray-3 disabled:hover:opacity-100"
	><slot /></button
>
