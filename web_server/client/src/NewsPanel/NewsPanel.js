import React from 'react';
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
// utility for debouncing
import _ from 'lodash';
import Auth from '../Auth/Auth';


class NewsPanel extends React.Component {
    constructor() {
        // just good habit, not make a difference here
        super();
        // pageNum is for pagination
        // loadAll is indicating whether we reach the ends of our news for this user
        this.state = { news:null, pageNum:1, loadAll:false };    
    }

    // @overirde
    // execution lifecycle: after constructor, then render, then this function
    componentDidMount() {
        this.loadMoreNews();
        // debouncing
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        window.addEventListener('scroll', () => this.handleScroll());
    }

    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
          console.log('Handle Scroll.');
          this.loadMoreNews();
        }
      }

    renderNews() {
        const news_list = this.state.news.map((news) => {
            // for each news
            // key is recommended     
            // { news } is not the one in this.state, but input of this function
            return (
                <a className='list-group-item' href='#'>
                    <NewsCard news={news} />
                </a>
            );
        });
        return (
            <div classname='container-fluid'>
                <div className = 'list-group'>
                    {news_list}
                </div>
            </div>
        );
    }


    // get news from server
    // it is get "more" news, this has state
    loadMoreNews() {
      if (this.state.loadAll == true){
        return;
      }

      console.log('Loading more news!');
      // REST API from Node backend server
      // Auth.getEmail get you the userid
      // see backend server rpc_client and routes for this REST API
      const news_url = 'http://' + window.location.hostname + ':3000' +
                       '/news/userId=' + Auth.getEmail() + '&pageNum=' + this.state.pageNum;
      // encode is used because whatif a user name is &page, it will attack our server
      // encode will replace special char with some random char 
      const request = new Request(encodeURI(news_url), {
        method:'GET',
        headers: {
          'Authorization': 'bearer ' + Auth.getToken(),
          }
        });
  
      fetch(request)
        .then(res => res.json())
        .then(new_news => {
          if (!new_news || new_news.length == 0) {
            this.setState({loadedAll:true});
          }
          this.setState({
            news: this.state.news ? this.state.news.concat(new_news) : new_news,
            pageNum: this.state.pageNum + 1,
          });
        });
      }
    
    render() {
        if (this.state.news) {
          return (
            <div>
              {this.renderNews()}
            </div>
          );
        } else {
          return (
            <div>
              Loading...
            </div>
          );
        }
      }
}

export default NewsPanel;