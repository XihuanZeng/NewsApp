import React from 'react';
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
// utility for debouncing
import _ from 'lodash';

class NewsPanel extends React.Component {
    constructor() {
        // just good habit, not make a difference here
        super();
        this.state = { news:null };    
    }

    renderNews() {
        const news_list = this.state.news.map((news) => {
            // for each news
            // key is recommeded
            return (
                <a className='list-group-item' key={news.digest} href='#'>
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

    // @overirde
    // execution lifecycle: after constructor, then render, then this function
    componentDidMount() {
        this.loadMoreNews();
        // debouncing
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        window.addEventListener('scroll', () => this.handleScroll());
    }

    // get news from server
    // it is get "more" news, this has state
    loadMoreNews() {
        console.log('Loading more news!');
        const news_url = 'http://' + window.location.hostname + ':3000' + '/news'
        const request = new Request(news_url, { method:'GET' });
    
        fetch(request)
          .then(res => res.json())
          .then(new_news => {
            this.setState({
              news: this.state.news ? this.state.news.concat(new_news) : new_news,
            });
          });
      }
    
    render() {
        // if have news
        // render to NewsCard Component
        if (this.state.news){
            return (
                <div>
                    {this.renderNews()}
                </div>
            )
        } else {
            <div>
                Loading...
            </div>
        };
    };
}

export default NewsPanel;