var Editor = React.createClass({
    getInitialState: function () {
        if(window.localStorage){
            var saved_post = window.localStorage.getItem(storage_key);
            if(saved_post){
                return JSON.parse(saved_post);
            }
        }
        return {
            slug: init_slug,
            title: init_title,
            content: init_content,
            tags: init_tags,
            content_style: {height: '100px'}
        }
    },
    rawMarkup: function() {
        marked.setOptions({
            highlight: function (code) {
                return hljs.highlightAuto(code).value;
            }
        });
        return { __html: marked(this.state.content) };
    },
    handleChange: function () {
        this.setState({
            title:this.refs.title_field.value,
            content:this.refs.textarea.value,
            tags:this.refs.tag_field.value.split(','),
            slug: this.refs.slug_field.value,
            content_style: {height: this.refs.textarea.scrollHeight}
        });
        if(window.localStorage){
            window.localStorage.setItem(storage_key, JSON.stringify(this.state));
        }
    },
    handelSubmit: function(){
        $.ajax({
            type: "POST",
            url: window.location.pathname,
            async: false,
            data: JSON.stringify(this.state),
            dataType: "json",
            success: function(data) {
                if(data['slug']){
                    window.localStorage.removeItem(storage_key);
                    window.location.href = "/";
                }
            }
        });
    },
    render: function () {
        return (
            <div className="editor">
                <div className="post">
                    <h2 className="title" id="title">
                        <a href="#">{this.state.title}</a>
                    </h2>
                    <div
                        className="post_body yue"
                        dangerouslySetInnerHTML={this.rawMarkup()}
                        >
                    </div>
                    <div className="info">
                    <span className="tags" id="tag">
                        <i className="fa fa-tags"></i>
                        {this.state.tags.map(function(tag, i){
                            return (
                                <a key={i} href="#">{tag}</a>
                            );
                        })}
                    </span>
                    </div>
                </div>
                <div className="fields">
                    <input
                        className="editor-title"
                        defaultValue={this.state.title}
                        type="text"
                        ref="title_field"
                        onChange={this.handleChange}
                        />
                    <textarea
                        className="editor-content"
                        style={this.state.content_style}
                        defaultValue={this.state.content}
                        ref="textarea"
                        onChange={this.handleChange}>
                    </textarea>
                    <input
                        className="editor-tags"
                        defaultValue={this.state.tags}
                        type="text"
                        ref="tag_field"
                        onChange={this.handleChange}
                        />
                    <input
                        className="editor-slug"
                        defaultValue={this.state.slug}
                        type="text"
                        ref="slug_field"
                        onChange={this.handleChange}
                        />
                    <input
                        className="editor-submit"
                        type="submit"
                        onClick={this.handelSubmit}
                        value="SUBMIT"
                        >
                    </input>
                </div>
            </div>
        )
    }
});

ReactDOM.render(<Editor />, document.getElementById('editor'));