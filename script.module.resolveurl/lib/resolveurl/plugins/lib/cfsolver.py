'''
    Kodi resolveurl plugin
    Copyright (C) 2019 script.module.resolveurl
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
 
# Based on cfscrape.py, credits to Team Universal.
# https://github.com/teamuniversal/scrapers/blob/master/_modules4all/script.module.universalscrapers/lib/universalscrapers/modules/cfscrape.py
 
def test_cloudflare(response, content):
    '''
    :param response: HttpResponse object from the Net module.
    :param content: '.content' attribute of the response object.
    '''
    if response._response.code == 503:
        info = response._response.info()
        return 'Server' in info and info.getheader('Server').startswith('cloudflare') and 'jschl_vc' in content
    return False
    
 
def solve_cf_challenge(response, content):
    '''
    :param response: HttpResponse object from the resolveurl.lib.net module.
    :param content: '.content' attribute of the HTTPResponse object (since it can only be read once, it's
    sent by the caller).
    :returns: The solution URL that will take you to the right page, or None if it failed solving it.
    
    Example use:
    
        from resolveurl.common import Net
        from resolveurl.lib.net import HttpResponse
        myNet = Net()
        try:
            r = myNet.http_GET(url, headers=myHeaders)
        except HTTPError as e:
            r = HttpResponse(e)
            content = r.content
            if cfsolver.test_cloudflare(r, content): # Test if there's a Cloudflare challenge.
                submitURL = cfsolver.solve_cf_challenge(r, content) # Get the solution URL.
                if not submitURL:
                    return None
                # Get redirected to the proper page.
                myHeaders['Referer'] = r.get_url() + '/'
                r = myNet.http_GET(submitURL, headers=myHeaders)
                content = r.content # This is the right content.
    '''
    import re
    from urllib import urlencode
    from urlparse import urlparse    
    from xbmc import sleep as xbmcSleep   
    
    def _parseJSString(s):
        try:
            offset=1 if s[0]=='+' else 0
            val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
            return val
        except:
            return None
    
    # Cloudflare requires a delay before solving the challenge.
    xbmcSleep(7000) # In milliseconds.
    
    body = content
    original_url = response.get_url()
    parsed_url = urlparse(original_url)
    domain = parsed_url.netloc
    submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, domain)
 
    params = { }
    
    try:
        params['jschl_vc'] = re.search(r'name="jschl_vc" value="(\w+)"', body).group(1)
        params['pass'] = re.search(r'name="pass" value="(.+?)"', body).group(1)
 
        # Extract the arithmetic operation.
        init = re.findall('setTimeout\(function\(\){\s*var\s*.*?.*:(.*?)}', body)[-1]
        builder = re.findall(r"challenge-form\'\);\s*(.*)a.v", body)[0]
        if '/' in init:
            init = init.split('/')
            decryptVal = _parseJSString(init[0]) / float(_parseJSString(init[1]))
        else:
            decryptVal = _parseJSString(init)
        lines = builder.split(';')
 
        for line in lines:
            if len(line)>0 and '=' in line:
                sections=line.split('=')
                if '/' in sections[1]:
                    subsecs = sections[1].split('/')
                    line_val = _parseJSString(subsecs[0]) / float(_parseJSString(subsecs[1]))
                else:
                    line_val = _parseJSString(sections[1])
                decryptVal = float(eval(('%.16f'%decryptVal)+sections[0][-1]+('%.16f'%line_val)))
 
        params["jschl_answer"] = str(float('%.10f'%decryptVal) + len(domain))        
        return submit_url + '?' + urlencode(params)
        
    except:
        return None