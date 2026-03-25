/**
 * Array utility snippets for common array operations.
 */

/**
 * Split an array into chunks of a given size.
 * @example chunk([1, 2, 3, 4, 5], 2) // [[1, 2], [3, 4], [5]]
 */
function chunk(array, size) {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}

/**
 * Flatten a nested array of arbitrary depth.
 * @example deepFlatten([1, [2, [3, [4]]]]) // [1, 2, 3, 4]
 */
function deepFlatten(array) {
  return array.reduce(
    (flat, item) =>
      Array.isArray(item) ? flat.concat(deepFlatten(item)) : flat.concat(item),
    []
  );
}

/**
 * Return unique elements from an array, preserving insertion order.
 * @example unique([1, 2, 2, 3, 1]) // [1, 2, 3]
 */
function unique(array) {
  return [...new Set(array)];
}

/**
 * Return unique elements using a key function (e.g. for objects).
 * @example uniqueBy([{id:1},{id:2},{id:1}], x => x.id) // [{id:1},{id:2}]
 */
function uniqueBy(array, keyFn) {
  const seen = new Set();
  return array.filter((item) => {
    const key = keyFn(item);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/**
 * Group an array of objects by a key function.
 * @example groupBy([{type:'a'},{type:'b'},{type:'a'}], x => x.type)
 *          // { a: [{type:'a'},{type:'a'}], b: [{type:'b'}] }
 */
function groupBy(array, keyFn) {
  return array.reduce((groups, item) => {
    const key = keyFn(item);
    (groups[key] ??= []).push(item);
    return groups;
  }, {});
}

/**
 * Compute the sum of an array of numbers (or using a selector function).
 * @example sum([1, 2, 3]) // 6
 * @example sum([{v:1},{v:2}], x => x.v) // 3
 */
function sum(array, fn = (x) => x) {
  return array.reduce((acc, item) => acc + fn(item), 0);
}

/**
 * Return a random element from an array.
 */
function sample(array) {
  return array[Math.floor(Math.random() * array.length)];
}

/**
 * Shuffle an array in-place using the Fisher-Yates algorithm and return it.
 */
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

/**
 * Compute the difference of two arrays (elements in a but not in b).
 * @example difference([1, 2, 3, 4], [2, 4]) // [1, 3]
 */
function difference(a, b) {
  const setB = new Set(b);
  return a.filter((item) => !setB.has(item));
}

/**
 * Compute the intersection of two arrays.
 * @example intersection([1, 2, 3], [2, 3, 4]) // [2, 3]
 */
function intersection(a, b) {
  const setB = new Set(b);
  return a.filter((item) => setB.has(item));
}

/**
 * Zip multiple arrays together into an array of tuples.
 * @example zip([1, 2], ['a', 'b']) // [[1, 'a'], [2, 'b']]
 */
function zip(...arrays) {
  const length = Math.min(...arrays.map((a) => a.length));
  return Array.from({ length }, (_, i) => arrays.map((a) => a[i]));
}

module.exports = {
  chunk,
  deepFlatten,
  unique,
  uniqueBy,
  groupBy,
  sum,
  sample,
  shuffle,
  difference,
  intersection,
  zip,
};
