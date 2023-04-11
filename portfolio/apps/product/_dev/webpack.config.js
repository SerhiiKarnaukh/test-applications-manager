const MiniCssExtractPlugin = require('mini-css-extract-plugin'),
  { CleanWebpackPlugin } = require('clean-webpack-plugin'),
  TerserWebpackPlugin = require('terser-webpack-plugin'),
  CssMinimizerPlugin = require('css-minimizer-webpack-plugin'),
  path = require('path'),
  bundleDirName = 'bundle',
  bundlePath = `../static/product/${bundleDirName}`,
  isDev = process.env.NODE_ENV === 'development',
  isProd = !isDev

const cssLoaders = (extra) => {
  const loaders = [
    {
      loader: MiniCssExtractPlugin.loader,
      options: {
        publicPath: '',
      },
    },
    'css-loader',
    {
      loader: 'postcss-loader',
      options: {
        postcssOptions: {
          plugins: [['postcss-preset-env']],
        },
      },
    },
  ]

  if (extra) {
    loaders.push(extra)
  }
  return loaders
}

const babelOptions = (preset) => {
  const opts = {
    presets: ['@babel/preset-env'],
    plugins: ['@babel/plugin-proposal-class-properties'],
  }

  if (preset) {
    opts.presets.push(preset)
  }
  return opts
}

module.exports = {
  mode: 'development',
  entry: {
    jquery: [
      '@babel/polyfill/noConflict',
      path.resolve(__dirname, 'vendors/jquery'),
    ],
    bootstrap: [
      '@babel/polyfill/noConflict',
      path.resolve(__dirname, 'vendors/bootstrap/bootstrap'),
    ],
    index: [
      '@babel/polyfill/noConflict',
      path.resolve(__dirname, 'layouts/index/index'),
    ],
  },
  output: {
    publicPath: `${bundlePath}/`,
    path: path.resolve(__dirname, bundlePath),
    filename: '[name].js',
  },
  devtool: isDev ? 'source-map' : false,

  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
    }),
    // new FaviconsWebpackPlugin({
    //     logo: './resources/images/favicon.svg',
    //     cache: true,
    //     prefix: '../bundle',
    //     inject: false,
    //     favicons: {
    //         appName: 'Beautifl',
    //         appDescription: 'Discover the ultimate hair and wig shopping experience',
    //         background: '#ffffff',
    //         theme_color: '#EC709A',
    //         icons: {
    //             coast: false,
    //             yandex: false
    //         }
    //     }
    // }),
    new CleanWebpackPlugin(),
  ],

  module: {
    rules: [
      //JS
      {
        test: /\.m?js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: babelOptions(),
        },
      },
      // CSS
      {
        test: /\.css$/,
        use: cssLoaders(),
      },
      // SCSS
      {
        test: /\.s[ac]ss$/,
        use: cssLoaders('sass-loader'),
      },
      // Fonts
      {
        test: /\.woff2?$/i,
        type: 'asset/resource',
        generator: {
          filename: './[name][ext]',
        },
      },
      // Resources
      // {
      //     test: /.(jpe?g|png|svg|gif|woff(2)?|eot|ttf)(\?[a-z0-9=]\.+)?$/,
      //     oneOf: [
      //         {
      //             resourceQuery: /inline-css/,
      //             use: 'url-loader'
      //         },
      //         {
      //             resourceQuery: /inline-js/,
      //             use: 'svg-inline-loader'
      //         },
      //         {
      //             use: 'file-loader?name=./[name].[ext]'
      //         }
      //     ]
      // },
    ],
  },
  optimization: {
    minimizer: [new TerserWebpackPlugin(), new CssMinimizerPlugin()],
  },
}
