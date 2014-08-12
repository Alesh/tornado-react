function render_jsx(jsx_name, props) {
    props = eval('('+props+')');
    var React = require("react");
    var component = require(jsx_name);
    if (component) 
        return React.renderComponentToString(component(props));
    else
        return 'Error'
}