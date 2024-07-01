<template>
  <section id="contact" class="section-auth section-bg wow fadeInUp" style="visibility: visible; animation-name: fadeInUp;">
    <div class="container">
      <div class="section-header">
        <h2>Articles</h2>
      </div>
      <div class="row justify-content-center">
        <div class="col-lg-4 mb-4" v-for="article in articles" :key="article.ID_Article">
          <div class="card mb-lg-0">
            <img v-if="article.Contenu_Article.includes('<img')" :src="extractImageSrc(article.Contenu_Article)" class="img card-img-top" alt="Article Image">
            <div class="publication-date">
              <div class="date-circle blue-circle">{{ formatDateCircle(article.Date_Publication_A, 'day') }}</div>
              <div class="date-circle red-circle">{{ formatDateCircle(article.Date_Publication_A, 'month') }}</div>
              <div class="date-circle green-circle">{{ formatDateCircle(article.Date_Publication_A, 'year') }}</div>
            </div>
            <div class="card-body">
              <h5 class="card-title text-muted text-uppercase text-center">{{ article.Titre_Article }}</h5>
              <p class="card-text text-muted" v-html="truncateContent(extractContent(article.Contenu_Article))"></p>
              <hr class="hr-article">
              <div class="text-center">
                <a :href="'/article/' + encryptId(article.ID_Article)" class="article-btn btn btn-blue">Lire article</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { encryptId } from '../utils';

export default {
  data() {
    return {
      articles: []
    };
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    async fetchArticles() {
      try {
        const response = await fetch('/api/articles/');
        const articles = await response.json();

        articles.forEach(article => {
          article.Contenu_Article = article.Contenu_Article.replace(/src="/g, 'src="http://localhost:8000');
        });

        this.articles = articles.sort((a, b) => new Date(b.Date_Publication_A) - new Date(a.Date_Publication_A));
      } catch (error) {
        console.error('Erreur lors de la récupération des articles:', error);
      }
    },
    truncateContent(content) {
      return content.length > 150 ? content.substring(0, 150) + '...' : content;
    },
    extractContent(content) {
      return content.replace(/<[^>]+>/g, '');
    },
    extractImageSrc(content) {
      const regex = /<img.*?src=["'](.*?)["']/;
      const match = regex.exec(content);
      return match ? match[1] : '';
    },
    formatDateCircle(date, part) {
      const d = new Date(date);
      switch (part) {
        case 'day':
          return d.getDate();
        case 'month':
          return d.getMonth() + 1;
        case 'year':
          return d.getFullYear();
        default:
          return '';
      }
    },
    encryptId(id) {
      return encryptId(id);
    }
  }
};
</script>

<style lang="scss">
.section-header {
  text-align: center;
  margin-bottom: 2rem;
}
.card {
  margin: 0;

}

</style>