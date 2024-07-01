<template>
    <section id="speakers-details" class="section-auth wow fadeIn">
      <div class="container" v-if="article">
        <div class="section-header">
          <h2>{{ article.Titre_Article }}</h2>
          <p>{{ formatDate(article.Date_Publication_A) }}</p>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="details">
              <p v-html="article.Contenu_Article"></p>
            </div>
          </div>
        </div>
      </div>
    </section>
  
    <section id="gallery" class="wow fadeInUp" v-if="articleImages.length > 0">
      <div class="container">
        <div class="section-header">
          <h2>Gallery</h2>
          <p>Check our gallery from the recent events</p>
        </div>
      </div>
      <div class="owl-carousel gallery-carousel">
        <a v-for="(image, index) in articleImages" :key="index" :href="image" class="venobox" :data-gall="'gallery-carousel' + index"><img class="img" :src="image" alt=""></a>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    props: ['id'],
    data() {
      return {
        article: {},
        articleImages: []
      };
    },
    created() {
      this.fetchArticleDetails();
    },
    methods: {
      async fetchArticleDetails() {
  try {
    const response = await fetch(`/api/article-detail/${this.id}/`);
    this.article = await response.json();
    this.article.Contenu_Article = this.article.Contenu_Article.replace(/src="/g, 'src="http://localhost:8000');
    this.extractImagesFromContent();
  } catch (error) {
    console.error('Error fetching article details:', error);
  }
},
      extractImagesFromContent() {
        const regex = /<img.*?src=["'](.*?)["']/g;
        const images = [];
        let match;
        while ((match = regex.exec(this.article.Contenu_Article)) !== null) {
          images.push(match[1]);
        }
        this.articleImages = images.slice(0, 8); // Limit to 8 images
      },
      formatDate(date) {
        return new Date(date).toLocaleString();
      },
      extractImageSrc(content) {
  const regex = /<img.*?src=["'](.*?)["']/;
  const match = regex.exec(content);
  if (match && match[1]) {
    return match[1];
  } else {
    return '';
  }
}
    }
  };
  </script>
  
  <style>
  /* Styles spécifiques au composant */
  .img {
    max-width: 60%!important;
    height: 100px!important;
    margin-right: 10px !important;
  }
  </style>