const { EleventyHtmlBasePlugin } = require("@11ty/eleventy");

module.exports = function(eleventyConfig) {
  eleventyConfig.addPlugin(EleventyHtmlBasePlugin);

  eleventyConfig.addPassthroughCopy("src/assets/css");
  eleventyConfig.addPassthroughCopy("src/assets/js");
  eleventyConfig.addPassthroughCopy("src/assets/img");
  eleventyConfig.addPassthroughCopy("src/assets/fonts");
  eleventyConfig.addPassthroughCopy("src/assets/splide");
  eleventyConfig.addPassthroughCopy("src/assets/organ-concerts");
  eleventyConfig.addPassthroughCopy("src/assets/organ-concerts-hiiden");
  eleventyConfig.addPassthroughCopy(".nojekyll");
  eleventyConfig.addPassthroughCopy("CNAME");

  eleventyConfig.addGlobalData("site", {
    title: "Хийденвуори.рф",
    url: "https://xn--b1addkdc4ajs2ap.xn--p1ai",
    subtitle: "Туристическое пространство на Ладожском озере!",
    phone1: "+7 (921) 014-11-90",
    phone2: "+7 (921) 014-64-47",
    phone1Raw: "+79210141190",
    phone2Raw: "+79210146447",
    email: "mail@hiidenvuori.ru",
    address: "Республика Карелия, д. Хийденсельга",
    ymId: 103525753,
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    templateFormats: ["njk", "html", "md"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
