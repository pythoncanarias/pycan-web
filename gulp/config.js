import path from 'path';


function getNodeModulesPathFrom(module_name)
{
  let module_path = require.resolve(module_name);
  while(module_path !== '/' && path.basename(module_path) !== "node_modules")
  {
    module_path = path.dirname(module_path);
  }
  return module_path;
}


const APPS = [
  "commons",
  "events",
  "homepage",
  "about",
  "legal",
  "members",
  "jobs",
];

const NODE_MODULES_DIR = getNodeModulesPathFrom('@fortawesome/fontawesome-free');

const LIBS = {
  CSS: {
    commons: [NODE_MODULES_DIR + "/@fortawesome/fontawesome-free/css/all.css"],
    homepage: ["homepage/static/homepage/css/vendor.scss"],
  },
  JS: {},
};

export { APPS, LIBS, NODE_MODULES_DIR };
