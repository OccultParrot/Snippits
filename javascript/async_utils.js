/**
 * Async utility snippets for working with Promises and async/await.
 */

/**
 * Wait for a given number of milliseconds.
 * @example await sleep(500); // pause for 500 ms
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Retry an async function up to maxAttempts times with an optional delay between attempts.
 * @param {() => Promise<T>} fn - The async function to retry.
 * @param {number} maxAttempts - Maximum number of attempts (default 3).
 * @param {number} delayMs - Delay in ms between retries (default 1000).
 * @returns {Promise<T>}
 * @example
 *   const data = await retry(() => fetch(url).then(r => r.json()), 3, 500);
 */
async function retry(fn, maxAttempts = 3, delayMs = 1000) {
  let lastError;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt < maxAttempts) {
        await sleep(delayMs);
      }
    }
  }
  throw lastError;
}

/**
 * Wrap a Promise so that it rejects with a timeout error if not resolved within ms milliseconds.
 * @example const result = await withTimeout(fetch(url), 5000);
 */
function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error(`Timed out after ${ms}ms`)), ms)
  );
  return Promise.race([promise, timeout]);
}

/**
 * Run an array of async tasks with a concurrency limit.
 * @param {Array<() => Promise<T>>} tasks - Array of async task functions.
 * @param {number} limit - Maximum number of concurrent tasks.
 * @returns {Promise<T[]>} Results in the same order as the input tasks.
 * @example
 *   const results = await limitConcurrency(urls.map(url => () => fetch(url)), 5);
 */
async function limitConcurrency(tasks, limit) {
  const results = new Array(tasks.length);
  let nextIndex = 0;

  async function worker() {
    while (nextIndex < tasks.length) {
      const index = nextIndex++;
      results[index] = await tasks[index]();
    }
  }

  const workers = Array.from({ length: Math.min(limit, tasks.length) }, worker);
  await Promise.all(workers);
  return results;
}

/**
 * Memoize an async function, caching the result of each unique set of arguments.
 * @example
 *   const cachedFetch = memoizeAsync(url => fetch(url).then(r => r.json()));
 *   await cachedFetch('/api/user'); // fetches
 *   await cachedFetch('/api/user'); // returns cached result
 */
function memoizeAsync(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (!cache.has(key)) {
      cache.set(key, fn.apply(this, args));
    }
    return cache.get(key);
  };
}

/**
 * Sequentially resolve an array of Promises and return all results.
 * Unlike Promise.all, tasks start one after the other rather than all at once.
 * @example const results = await sequential([fetchA, fetchB, fetchC]);
 */
async function sequential(tasks) {
  const results = [];
  for (const task of tasks) {
    results.push(await task());
  }
  return results;
}

module.exports = { sleep, retry, withTimeout, limitConcurrency, memoizeAsync, sequential };
