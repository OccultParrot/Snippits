
/**
 * Layout component that wraps all routes with common header and footer elements.
 * Uses React Router's Outlet component to render nested route content.
 *
 * @returns {ReactElement} A div containing the header, main content area with Outlet, and footer
 */
function Layout(): ReactElement {

  return (
    <div className="flex min-h-screen flex-col">
      <main className="grow bg-white">
        <Outlet/>
      </main>
    </div>
  );
}


/**
 * Main application component that sets up routing configuration.
 * Implements a BrowserRouter with nested routes and error handling.
 *
 * @returns {ReactElement} The configured router with all application routes
 *
 * @desc
 * Routes structure:
 * - "/" (Layout wrapper)
 *   - "/" (index) -> Landing page
 *   - Dynamic routes from typeScriptConfigs array
 *   - "*" -> ErrorPage page for unmatched routes
 */
export default function App(): ReactElement {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <Layout/> }>
          {/* The "index" page is the one that gets served when you have a blank path */ }
          <Route index element={ pages[0].element }/>

          {/* Flatten all routes */ }
          { pages.slice(1).map(( pageProps: IPageProps ) => {
            if (!pageProps.children) {
              return <Route key={ pageProps.path } path={ pageProps.path } element={ pageProps.element }/>;
            }

            return (
              <Fragment key={ pageProps.path }>
                <Route path={ pageProps.path } element={ pageProps.element }/>
                { pageProps.children.map(( childProps ) => (
                  <Route
                    key={ `${ pageProps.path }/${ childProps.path }` }
                    path={ `${ pageProps.path }/${ childProps.path }` }
                    element={ childProps.element }
                  />
                )) }
              </Fragment>
            );
          }) }

          {/* The error page gets served if the path the user goes to does not exist. */ }
          <Route path="*" element={ <ErrorPage/> }/>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

import { type ReactElement } from 'react';

/**
 * Interface defining the properties for creating routes in the application.
 * Used by the CreateRoute function to generate route elements recursively.
 *
 * @interface IPageProps
 * @property {string} name - Used for the header menu to travel to that page
 * @property {string} path - The URL path segment for this route
 * @property {ReactElement} element - The React component to render at this route
 * @property {IPageProps[]} [children] - Optional nested routes under this route
 */
export interface IPageProps {
  name: string;
  path: string;
  isHidden?: boolean;
  isAdminOnly?: boolean;
  element: ReactElement;
  children?: IPageProps[];
}

import type { IPageProps } from "../types.ts";

import LandingPage from "../pages/LandingPage.tsx";

/**
 * Configuration array defining all application routes.
 * Each entry maps to a route in the application, along with getting a link to the path in the nav bar if marked false for isHidden
 *
 * Also, the first item in the array is considered the "root" and the title will redirect to it.
 * @type {Array<IPageProps>}
 * @example
 * {
 *   name: "home",
 *   path: "home",
 *   isHidden?: false
 *   element: <Home/>,
 *   children: [] // optional nested routes
 * }
 */
export const pages: Array<IPageProps> = [
  {
    name: "Landing Page",
    path: "",
    element: <LandingPage/>,
  }
]
