import dash
from dash import dcc, html, Input, Output, State, ALL
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import os


# ==================== 0. Base64 图片读取函数 ====================
def get_image_base64(filename):
    """
    自动获取 assets 文件夹内图片的完整绝对路径，并转换为 Base64 编码字符串。
    """
    filepath = os.path.join(os.path.dirname(__file__), 'assets', filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
    print(f"⚠️ [未找到图片文件]: {filepath}")
    return ""


# ==================== 1. 全球篮球传播数据源 ====================
start_pt = {"name": "Springfield College, USA", "lat": 42.1015, "lon": -72.5898, "year": 1891}

history_data = [
    {
        "id": 0, "country_code": "FRA", "name": "France", "display_name": "France", "lat": 48.8566, "lon": 2.3522,
        "color": "#d97706", "start_year": 1893,
        "leader": "Mel Rideout / Renato William Jones / James Naismith",
        "photo": "france.png",
        "desc": "<b>1893 (Introduction to Europe):</b> Mel Rideout, a former student of Dr. James Naismith at Springfield College, officially introduced basketball to Europe by organizing the continent's first game at the YMCA on Rue de Trévise in Paris. The gymnasium on Rue de Trévise remains open today as the world's oldest continuously operating indoor basketball court.<br><br>"
                "<b>WWI Trench Catalyst (1917–1919):</b> Following the entry of the United States into World War I in 1917, Dr. James Naismith, aged 53, traveled to the French Western Front as a YMCA war work secretary. Naismith set up peach baskets and makeshift backboards in military camps and staging areas to boost troop morale and enrich trench life. This wartime initiative rapidly popularized basketball among European soldiers. In 1919, Paris hosted the landmark Inter-Allied Games, where the victorious US military squad displayed advanced team tactics, sowing the seeds for local basketball clubs across France.<br><br>"
                "<b>International Governing Architecture (1932–1936):</b> R. William Jones co-founded the International Basketball Federation (FIBA) in Europe in 1932. Jones successfully advocated for basketball's inclusion as an official medal sport at the 1936 Berlin Olympic Games, where Naismith was personally invited to award the inaugural medals.<br><br>"
                "<b>Domestic Diffusion & Professional Growth:</b> From Paris, the sport rapidly expanded southward to Marseille and Lyon, and northward to Lille and Bordeaux. Regional basketball associations flourished throughout the 1920s. Today, France's LNB Pro A stands as one of Western Europe's premier domestic leagues, nurturing elite international talent like Victor Wembanyama and Tony Parker, while cementing France as a global basketball powerhouse."
    },
    {
        "id": 1, "country_code": "GBR", "name": "United Kingdom", "display_name": "UK", "lat": 51.5074, "lon": -0.1278,
        "color": "#dc2626", "start_year": 1894,
        "leader": "Dr. James Naismith / Martina Bergman-Österberg",
        "photo": "uk.png",
        "desc": "<b>1894 (Arrival via the YMCA Network):</b> Basketball crossed the Atlantic to the United Kingdom just three years after its invention. Brought over by YMCA physical instructors, the sport was initially received with great enthusiasm in physical training colleges across London.<br><br>"
                "<b>Evolution of Netball:</b> Due to Victorian social etiquette and restrictive long skirts worn by female athletes at the time, physical education pioneer Martina Bergman-Österberg and local instructors modified Naismith's original 13 rules. Dribbling was replaced with mandatory passing, physical contact was strictly restricted, and backboards were removed. This adapted sport evolved into 'Netball', becoming a major standalone sport that remains exceptionally popular across women's athletic programs throughout the British Commonwealth today.<br><br>"
                "<b>Domestic Regional Expansion & Modern League:</b> London served as the primary dissemination hub before basketball spread to industrial centers such as Manchester, Birmingham, Edinburgh, and Belfast. While Netball dominated physical education in schools, men's basketball built strong grassroots roots in urban areas. The British Basketball League (BBL) was established in 1987 to consolidate professional franchises, playing a vital role in developing basketball culture across the UK."
    },
    {
        "id": 3, "country_code": "CHN", "name": "China", "display_name": "China", "lat": 39.9042, "lon": 116.4074,
        "color": "#059669", "start_year": 1895,
        "leader": "David Willard Lyon / Dong Shouyi / Yao Ming",
        "photo": "china.png",
        "desc": "<b>1895 (Introduction to China):</b> David Willard Lyon arrived in Tianjin as the first official representative of the International YMCA, introducing basketball to East Asia. The first public demonstration match took place in Tianjin on January 11, 1896. By 1910, basketball was included as an official exhibition sport at the inaugural National Games in Nanjing.<br><br>"
                "<b>Institutionalization & Early Olympic Era:</b> Educator Dong Shouyi authored China's earliest sports textbooks and coached the Chinese national team at the 1936 Berlin Olympics. Following the founding of the People's Republic of China, Dong served as President of the Chinese Basketball Association (CBA), laying the structural groundwork for national officiating, youth academies, and elite sports schools.<br><br>"
                "<b>The Yao Ming Phenomenon (2002):</b> Yao Ming was selected as the #1 overall pick in the 2002 NBA Draft—the first international player without US college experience to achieve this honor. Across his Hall-of-Fame career with the Houston Rockets, Yao bridged global sports culture, attracting over 300 million Chinese viewers, driving the NBA's rapid expansion in Asia, and establishing the annual NBA China Games.<br><br>"
                "<b>Nationwide Grassroots & Professional Landscape:</b> From its origin in Tianjin, basketball spread to Shanghai, Guangzhou, and regional centers nationwide. Modern grassroots phenomena like the 'Village BA' (Taipan Village) demonstrate the profound cultural depth of rural basketball. Established in 1995, the CBA league operates alongside extensive university (CUBA) and youth programs, making basketball one of the most widely played sports across China."
    },
    {
        "id": 2, "country_code": "DEU", "name": "Germany", "display_name": "Germany", "lat": 52.5200, "lon": 13.4050,
        "color": "#7c3aed", "start_year": 1896,
        "leader": "Dr. James Naismith / Dirk Nowitzki",
        "photo": "germany.png",
        "desc": "<b>1896–1936 (Early Adoption & Olympic Milestone):</b> Introduced to Germany through physical culture exchanges in the late 1890s, basketball grew steadily alongside traditional gymnastics. The 1936 Berlin Olympics marked a monumental turning point: basketball made its official debut as an Olympic medal sport. Dr. James Naismith personally tossed the opening tip-off under rainy conditions, validating basketball on the global stage.<br><br>"
                "<b>Post-War Development & Dirk Nowitzki's Era:</b> Early German basketball centered in Berlin before expanding to Munich, Frankfurt, Stuttgart, and Hamburg. Following World War II, West Germany established a robust club system, while East Germany developed state-sponsored athletic institutes. Dirk Nowitzki revolutionized the game in the late 1990s and 2000s; his signature perimeter skill set as a 7-footer paved the way for modern stretch-bigs worldwide, leading the Dallas Mavericks to the 2011 NBA Championship.<br><br>"
                "<b>Modern European Dominance:</b> Reunified Germany's Basketball Bundesliga (BBL) has developed into one of Europe's premier professional leagues. Backed by world-class youth academies and club structures, the German national team captured the 2023 FIBA World Cup title, proving the strength of its long-term player development system."
    },
    {
        "id": 4, "country_code": "BRA", "name": "Brazil", "display_name": "Brazil", "lat": -23.5505, "lon": -46.6333,
        "color": "#2563eb", "start_year": 1900,
        "leader": "Augusto Shaw / Oscar Schmidt",
        "photo": "brazil.png",
        "desc": "<b>1900 (Gateway to South America):</b> Augusto Shaw, an American graduate from Yale University, brought basketball to Mackenzie College in São Paulo in 1900. Brazil became the pioneer nation to adopt and systematically spread basketball across South America, triggering widespread adoption across the continent.<br><br>"
                "<b>The Legend of Oscar Schmidt ('Mão Santa'):</b> Brazil birthed one of the greatest scoring legends in international basketball history, Oscar Schmidt. Known as 'Mão Santa' (The Holy Hand), Schmidt holds the absolute record for all-time points scored in Olympic history (1,093 points across 5 Games) and an unofficial career total of 49,737 points. In the 1987 Pan American Games final in Indianapolis, Schmidt scored 46 points to lead Brazil to a historic upset over the USA national team, handing the US its first-ever defeat on home soil.<br><br>"
                "<b>Domestic Growth & Regional Influence:</b> From São Paulo, basketball spread quickly to Rio de Janeiro, Brasília, and Belo Horizonte. Brazil formed one of the earliest national basketball federations in South America, winning World Championships in 1959 and 1963. The Novo Basquete Brasil (NBB) league maintains this legacy today, fostering elite South American talent."
    },
    {
        "id": 5, "country_code": "PHL", "name": "Philippines", "display_name": "Philippines", "lat": 14.5995,
        "lon": 120.9842,
        "color": "#b45309", "start_year": 1898,
        "leader": "Dionisio Calvo",
        "photo": "philippines.png",
        "desc": "<b>1898 (Rapid Asian Expansion):</b> Following the establishment of US administration in 1898, basketball was introduced into the public school system and YMCA programs across the Philippines. Its fast pace, minimal equipment requirements, and high accessibility made it instantly popular among local youth.<br><br>"
                "<b>Dionisio Calvo & Early International Success:</b> Sports pioneer Dionisio Calvo organized early national teams and helped establish international basketball structures in Asia. Under his leadership, the Philippines placed 5th at the 1936 Berlin Olympics—the highest Olympic finish by any Asian nation in basketball history.<br><br>"
                "<b>Asia's First Professional League & Mass Culture:</b> In 1975, the Philippine Basketball Association (PBA) was founded as Asia's first professional basketball league. Today, basketball is an integral part of everyday Filipino culture: outdoor courts line urban neighborhoods and rural villages from Manila to Cebu and Davao, making the Philippines one of the most passionate basketball nations in the world."
    },
    {
        "id": 7, "country_code": "USA", "name": "United States", "display_name": "USA", "lat": 40.7128, "lon": -74.0060,
        "color": "#4f46e5", "start_year": 1947,
        "leader": "Wat Misaka / David Stern / Michael Jordan",
        "photo": "usa.png",
        "desc": "<b>1947 (Breaking Barriers - Wat Misaka):</b> In 1947, Wataru 'Wat' Misaka joined the New York Knicks. Misaka, a Japanese-American WWII veteran who served in military intelligence, became the first non-white and first Asian player in NBA history, predating the entry of African-American players by three years and breaking early racial barriers in professional sports.<br><br>"
                "<b>Global Expansion & The 1992 Dream Team:</b> Under the guidance of NBA Commissioner David Stern (starting in 1984) and powered by Michael Jordan, basketball evolved into a multi-billion dollar global entertainment empire. The 1992 Barcelona Olympic 'Dream Team' captured international imaginations, uniting athletic excellence with global pop culture and inspiring generations of international players.<br><br>"
                "<b>Comprehensive Domestic Ecosystem:</b> Originating in Springfield, basketball expanded across major metropolitan hubs such as New York, Chicago, Los Angeles, and Indiana. Driven by High School hoops, college NCAA March Madness, the NBA/WNBA leagues, and iconic streetball sanctuaries like Harlem's Rucker Park, the US remains the structural heartbeat of global basketball."
    },
    {
        "id": 6, "country_code": "RUS", "name": "Russia (USSR)", "display_name": "Russia", "lat": 55.7558,
        "lon": 37.6173,
        "color": "#db2777", "start_year": 1958,
        "leader": "Sergei Belov / Alexander Gomelsky",
        "photo": "russia.png",
        "desc": "<b>1958 (Cultural Exchanges & Cold War Rivalry):</b> In 1958, the US and Soviet Union signed a bilateral cultural exchange agreement, launching a series of high-profile basketball exhibition tours. These games provided rare cultural touchpoints during the height of Cold War tensions.<br><br>"
                "<b>The 1972 Munich Olympic Controversy:</b> In the final three seconds of the 1972 Munich Olympic gold medal match, the Soviet Union dramatically defeated the United States 51–50, snapping America's 63-game Olympic win streak. The match remains one of the most famous and politically charged moments in international sports history.<br><br>"
                "<b>Sergei Belov's Legacy & State System:</b> Soviet superstar Sergei Belov led his national team through two decades of international excellence. In 1992, Belov became the first non-American player inducted into the Naismith Memorial Basketball Hall of Fame. Anchored by major sporting hubs in Moscow, Saint Petersburg, Kaunas, and Tbilisi, the Soviet state athletic system developed disciplined tactical systems that fundamentally shaped European basketball."
    },
    {
        "id": 8, "country_code": "RWA", "name": "Rwanda", "display_name": "Rwanda", "lat": -1.9403, "lon": 30.0619,
        "color": "#0891b2", "start_year": 2019,
        "leader": "Barack Obama / Masai Ujiri",
        "photo": "rwanda.png",
        "desc": "<b>2019–Present (Modern African Strategy & BAL):</b> Africa represents a vibrant frontier for global basketball development. In 2019, the NBA collaborated with FIBA to launch the Basketball Africa League (BAL) in Kigali, Rwanda—marking the NBA's first official league operation outside North America. Former US President Barack Obama joined NBA Africa as a strategic partner to support youth empowerment and sports infrastructure.<br><br>"
                "<b>Kigali Arena & Regional Impact:</b> The construction of the state-of-the-art BK Arena in Kigali has turned Rwanda's capital into a hub for international African basketball. Beyond elite competition, the BAL initiative focuses on economic development, sports diplomacy, and creating sustainable athletic opportunities for youth across the African continent."
    }
]

# 测验题目数据源
quiz_questions = [
    {
        "id": 0,
        "question": "1. In which year was basketball invented by Dr. James Naismith in Springfield?",
        "options": ["1889", "1891", "1895", "1900"],
        "answer": "1891"
    },
    {
        "id": 1,
        "question": "2. What is the standard height of the official basketball hoop globally?",
        "options": ["2.95 meters (9.5 ft)", "3.00 meters (9.8 ft)", "3.05 meters (10 ft)", "3.10 meters (10.2 ft)"],
        "answer": "3.05 meters (10 ft)"
    },
    {
        "id": 2,
        "question": "3. Who was the first non-white and first Asian player to play in the NBA history (1947)?",
        "options": ["Yao Ming", "Wat Misaka", "Wang Zhizhi", "Rui Hachimura"],
        "answer": "Wat Misaka"
    },
    {
        "id": 3,
        "question": "4. In which country was 'Netball' developed as an early adaptation of basketball for female players?",
        "options": ["United Kingdom", "France", "Germany", "Brazil"],
        "answer": "United Kingdom"
    },
    {
        "id": 4,
        "question": "5. Where was the Basketball Africa League (BAL) headquartered and established in 2019?",
        "options": ["Nairobi, Kenya", "Dakar, Senegal", "Kigali, Rwanda", "Cairo, Egypt"],
        "answer": "Kigali, Rwanda"
    }
]

df_dest = pd.DataFrame(history_data).sort_values("start_year")


def get_great_circle_points(lat1, lon1, lat2, lon2, num_pts=40):
    phi1, lam1 = np.radians(lat1), np.radians(lon1)
    phi2, lam2 = np.radians(lat2), np.radians(lon2)
    v1 = np.array([np.cos(phi1) * np.cos(lam1), np.cos(phi1) * np.sin(lam1), np.sin(phi1)])
    v2 = np.array([np.cos(phi2) * np.cos(lam2), np.cos(phi2) * np.sin(lam2), np.sin(phi2)])
    cos_omega = np.dot(v1, v2)
    omega = np.arccos(np.clip(cos_omega, -1.0, 1.0))
    if omega < 1e-6: return [lon1] * num_pts, [lat1] * num_pts
    lons, lats = [], []
    for ti in np.linspace(0, 1, num_pts):
        v_interp = (np.sin((1 - ti) * omega) / np.sin(omega)) * v1 + (np.sin(ti * omega) / np.sin(omega)) * v2
        lats.append(np.degrees(np.arcsin(v_interp[2])))
        lons.append(np.degrees(np.arctan2(v_interp[1], v_interp[0])))
    return lons, lats


# ==================== 2. Dash 页面样式与骨架 ====================
app = dash.Dash(__name__, update_title=None, suppress_callback_exceptions=True)
server = app.server

court_background_css = {
    'backgroundColor': '#f8fafc',
    'backgroundImage': 'radial-gradient(#e2e8f0 2px, transparent 2px), linear-gradient(to right, #f1f5f9 2px, transparent 2px), linear-gradient(to bottom, #f1f5f9 2px, transparent 2px)',
    'backgroundSize': '32px 32px, 64px 64px, 64px 64px',
    'color': '#1e293b',
    'fontFamily': '"Segoe UI", Arial, sans-serif',
    'minHeight': '100vh',
    'padding': '30px 30px 10px 30px',
    'display': 'flex',
    'flexDirection': 'column'
}

app.layout = html.Div(style=court_background_css, children=[
    html.Div(style={'flex': '1'}, children=[
        html.H1("Mega Basketball Chronicles (1891 - 2026)",
                style={'textAlign': 'center', 'color': '#0f172a', 'fontWeight': '800', 'marginBottom': '25px'}),

        dcc.Tabs(id="tabs-menu", value='tab-about', style={'fontWeight': 'bold'}, children=[
            dcc.Tab(label='About This Website', value='tab-about', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='History Overview', value='tab-overview', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='Interactive Globe', value='tab-globe', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='Country Archives', value='tab-countries', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='Interactive Quiz', value='tab-quiz', style={'backgroundColor': '#f1f5f9'}),
        ]),

        html.Div(id='tabs-content', style={
            'padding': '30px', 'backgroundColor': '#ffffff',
            'borderRadius': '0 0 12px 12px', 'boxShadow': '0 4px 20px rgba(0,0,0,0.05)',
            'border': '1px solid #e2e8f0', 'marginTop': '-1px'
        })
    ]),

    # 页脚版权标识
    html.Footer(
        children=[
            html.P("© 2026 Xiyuan Wan. All rights reserved.",
                   style={'textAlign': 'center', 'color': '#64748b', 'fontSize': '14px', 'margin': '0',
                          'fontWeight': '500'})
        ],
        style={
            'padding': '20px 0 10px 0',
            'borderTop': '1px solid #e2e8f0',
            'marginTop': '40px'
        }
    )
])


# ==================== 3. 多页面渲染回调 ====================
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-menu', 'value')
)
def render_tab_content(tab_name):
    if tab_name == 'tab-about':
        return html.Div(style={'maxWidth': '850px', 'margin': '0 auto'}, children=[
            html.H2("The Changing Landscape of Basketball Globalization",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px'}),

            html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '20px'},
                     children=[
                         html.Img(src=get_image_base64("nba_logo.png"),
                                  style={'maxHeight': '180px', 'objectFit': 'contain'}),
                         html.Img(src=get_image_base64("team_logos.png"),
                                  style={'maxHeight': '180px', 'objectFit': 'contain'})
                     ]),

            html.P(
                "As one of the four major professional sports leagues in North America, the NBA brings together the top basketball talents from around the world. Throughout the nearly 80-year history of the NBA, homegrown American players have historically dominated this competition. From prehistoric giants like Wilt Chamberlain, who set the legendary single-game 100-point record, to Michael Jordan, revered worldwide as the 'Air Jordan', and the relentlessly fiercely competitive Kobe Bryant—followed by the meteoric rise of 2010s superstars like LeBron James, Kevin Durant, and Stephen Curry—the absolute dominance of the United States on the Olympic stage has been undeniable.",
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify'}),

            html.Div(style={'textAlign': 'center', 'margin': '25px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("domestic.png"),
                         style={'maxWidth': '100%', 'maxHeight': '280px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),

            html.P(
                "However, in recent years, this narrative has shifted dramatically. The proportion of international players within the league has skyrocketed, with many not only proving their formidable skills but rapidly becoming the absolute franchise cornerstones within their first few seasons. The 'Greek Freak' Giannis Antetokounmpo, the otherworldly talent Victor Wembanyama, and the court maestro Nikola Jokić all hail from different corners of the globe and have captured numerous prestigious individual accolades. This global paradigm shift reached a boiling point during the 2024 Paris Olympics, where the Serbian national team led by Jokić and the French squad anchored by Wembanyama pushed Team USA to its absolute limits. Had it not been for the extraordinary, vintage heroics of James, Durant, and Curry, the coveted Olympic gold medal might have slipped from American hands.",
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify'}),

            html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'margin': '25px 0 15px 0'},
                     children=[
                         html.Img(src=get_image_base64("foreign1.png"),
                                  style={'maxHeight': '200px', 'objectFit': 'contain', 'borderRadius': '6px'}),
                         html.Img(src=get_image_base64("foreign2.png"),
                                  style={'maxHeight': '200px', 'objectFit': 'contain', 'borderRadius': '6px'})
                     ]),

            html.P(
                "This visualization serves as a testament to that evolution. Basketball is no longer a sport tethered exclusively to its birthplace or heavily centralized in one superpower nation. The rise of international powerhouses demonstrates that the language of basketball has truly broken down cultural boundaries, distributing elite expertise across continents and reshaping global sports diplomacy in the 21st century.",
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify', 'fontWeight': '500',
                       'color': '#0f172a'})
        ])

    elif tab_name == 'tab-overview':
        return html.Div(style={'maxWidth': '900px', 'margin': '0 auto'}, children=[
            html.H2("Origin & Global Development of Basketball",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px'}),

            html.Div(style={'textAlign': 'center', 'margin': '20px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("oldest_hoop.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),

            html.P(
                "Basketball was invented in December 1891 by Dr. James Naismith, a Canadian physical education instructor at the International YMCA Training School in Springfield, Massachusetts, USA. Tasked with creating a mild indoor winter sport for restless students, he drew inspiration from the folk game 'Duck-on-a-Rock'. He used two peach baskets and a soccer ball, drafted the original 13 fundamental rules, and hosted the world’s first basketball match on December 21, 1891. Most of his original rules remain the core framework of modern basketball.",
                style={'fontSize': '16px', 'lineHeight': '1.7'}),

            html.Div(style={'textAlign': 'center', 'margin': '25px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("evolution.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),

            html.P(
                "The standard height of the basketball hoop is exactly 3.05 meters (10 feet). When Dr. Naismith nailed the peach baskets to the gym balcony railing, the balcony was naturally 10 feet high. He never adjusted the height for balance and fairness, and this 10-foot height has been preserved as the global official standard for all competitive basketball courts ever since.",
                style={'fontSize': '16px', 'lineHeight': '1.7'}),

            html.Div(style={'textAlign': 'center', 'margin': '25px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("chamberlain.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),

            html.P(
                "The sport spread rapidly via the global YMCA network after 1893. It first reached Western Europe (France, UK), then East Asia (China, Philippines), Latin America (Brazil), and other continents. After World War I and World War II, basketball gained worldwide popularity. It became an official Olympic medal sport in 1936 Berlin. Later, the NBA was founded in 1947, growing into the world’s top professional league. FIBA standardized international competition rules, boosting transnational exchanges. In recent decades, basketball has evolved into a global mass sport with professional leagues, youth training systems and cultural diplomacy value across Africa, Europe, Asia and the Americas.",
                style={'fontSize': '16px', 'lineHeight': '1.7'})
        ])

    elif tab_name == 'tab-globe':
        standard_marks = {yr: f"{yr}" for yr in range(1890, 2031, 20)}
        return html.Div([
            html.Div(id='year-display-banner',
                     style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': 'bold', 'color': '#2563eb',
                            'marginBottom': '10px'}),
            html.Div([
                html.Label("Drag the slider to change timeline & rotate camera:",
                           style={'fontWeight': 'bold', 'color': '#475569', 'marginBottom': '8px', 'display': 'block'}),
                dcc.Slider(
                    id='timeline-slider',
                    min=1891, max=2026,
                    step=1,
                    marks=standard_marks,
                    value=1891,
                    updatemode='drag'
                )
            ], style={'padding': '20px', 'background': '#f8fafc', 'borderRadius': '8px', 'border': '1px solid #e2e8f0',
                      'marginBottom': '15px'}),

            # 居中容器，无边框与遮挡
            html.Div([
                dcc.Graph(
                    id='interactive-globe-graph',
                    style={'height': '68vh', 'width': '100%'},
                    config={'responsive': True, 'displayModeBar': False}
                )
            ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
        ])

    elif tab_name == 'tab-countries':
        dropdown_options = [{'label': row['name'], 'value': row['name']} for _, row in df_dest.iterrows()]
        return html.Div([
            html.Div([
                html.Label("Select a Country Archive:",
                           style={'fontWeight': 'bold', 'color': '#1e293b', 'marginRight': '15px'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=dropdown_options,
                    value=df_dest.iloc[0]['name'] if not df_dest.empty else None,
                    style={'width': '300px', 'display': 'inline-block', 'verticalAlign': 'middle'}
                )
            ], style={'marginBottom': '25px'}),
            html.Div(id='country-archive-display')
        ])

    elif tab_name == 'tab-quiz':
        return html.Div(style={'maxWidth': '800px', 'margin': '0 auto'}, children=[
            html.H2("🏀 Basketball Globalization Knowledge Quiz",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px',
                           'textAlign': 'center'}),
            html.P("Test your knowledge about the global history and evolution of basketball based on our archives!",
                   style={'textAlign': 'center', 'color': '#64748b', 'marginBottom': '30px'}),

            html.Div([
                html.Div(key=f"q-container-{q['id']}", style={
                    'backgroundColor': '#f8fafc', 'padding': '20px', 'borderRadius': '8px',
                    'marginBottom': '20px', 'border': '1px solid #e2e8f0'
                }, children=[
                    html.H4(q['question'], style={'color': '#0f172a', 'marginBottom': '12px'}),
                    dcc.RadioItems(
                        id={'type': 'quiz-options', 'index': q['id']},
                        options=[{'label': f" {opt}", 'value': opt} for opt in q['options']],
                        style={'display': 'flex', 'flexDirection': 'column', 'gap': '8px', 'fontSize': '15px'}
                    ),
                    html.Div(id={'type': 'quiz-feedback', 'index': q['id']}, style={'marginTop': '10px'})
                ]) for q in quiz_questions
            ]),

            html.Div(style={'textAlign': 'center', 'marginTop': '25px'}, children=[
                html.Button("Submit Answers", id="quiz-submit-btn", n_clicks=0,
                            style={'backgroundColor': '#2563eb', 'color': 'white', 'border': 'none',
                                   'padding': '12px 35px', 'fontSize': '16px', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontWeight': 'bold'}),
                html.Div(id="quiz-total-score", style={'marginTop': '20px', 'fontSize': '20px', 'fontWeight': 'bold'})
            ])
        ])


# ==================== 4. 动态地球逻辑（修复居中、平移与边框） ====================
@app.callback(
    [Output('interactive-globe-graph', 'figure'),
     Output('year-display-banner', 'children')],
    Input('timeline-slider', 'value')
)
def update_globe(selected_year):
    fig = go.Figure()

    # 透明底图层
    fig.add_trace(go.Choropleth(
        locations=["USA"], z=[0], colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
        showscale=False, geo='geo', hoverinfo='none'
    ))

    # 绘制源头 Springfield 节点
    fig.add_trace(go.Scattergeo(
        lon=[start_pt["lon"]], lat=[start_pt["lat"]], mode='markers+text',
        marker=dict(size=14, color='#ea580c', symbol='star'),
        text=["<b>Springfield (1891)</b>"], textposition="bottom center",
        textfont=dict(color="#ea580c", size=12),
        hoverinfo='none'
    ))

    active_countries = df_dest[df_dest["start_year"] <= selected_year]

    # 视角旋转经纬度设定（使用 rotation 代替 center，防止球体偏移与裁剪）
    rot_lat, rot_lon = start_pt["lat"], start_pt["lon"]
    if not active_countries.empty:
        latest_country = active_countries.iloc[-1]
        rot_lat, rot_lon = latest_country["lat"], latest_country["lon"]

    # 绘制线路与国家节点
    for _, row in active_countries.iterrows():
        mlons, mlats = get_great_circle_points(start_pt["lat"], start_pt["lon"], row["lat"], row["lon"])
        fig.add_trace(go.Scattergeo(
            lon=mlons, lat=mlats, mode='lines',
            line=dict(width=3, color=row["color"]), opacity=0.85, hoverinfo='none'
        ))

        fig.add_trace(go.Scattergeo(
            lon=[row["lon"]], lat=[row["lat"]], mode='markers+text',
            text=[f"<b>{row['display_name']} ({row['start_year']})</b>"],
            textposition="top center", textfont=dict(size=11, color='#1e293b'),
            marker=dict(size=9, color=row["color"]), hoverinfo='none'
        ))

    # 正确配置 3D 地球视角与无边框布局
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        geo=dict(
            scope='world',
            projection=dict(
                type='orthographic',
                rotation=dict(lon=rot_lon, lat=rot_lat, roll=0)
            ),
            showland=True, landcolor='#f1f5f9',
            showocean=True, oceancolor='#e0f2fe',
            showcountries=True, countrycolor='#cbd5e1',
            showframe=False,  # 隐藏图表正方形框线
            framecolor='rgba(0,0,0,0)',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # 消除画布内边距边框
        uirevision='dataset'  # 保持拖拽视角不被强行重置
    )
    return fig, f"🌍 Current Timeline Focus Year: {selected_year}"


# ==================== 5. 国家档案逻辑 ====================
@app.callback(
    Output('country-archive-display', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_archive(country_name):
    if not country_name:
        return html.Div("Please select a country from the dropdown menu.",
                        style={'padding': '20px', 'color': '#64748b'})

    filtered = df_dest[df_dest["name"] == country_name]
    if filtered.empty:
        return html.Div("Country data package not found.", style={'padding': '20px', 'color': '#ef4444'})

    row = filtered.iloc[0]

    country_fig = go.Figure()
    loc_list = [row["country_code"]]
    if row["country_code"] == "CHN":
        loc_list.append("TWN")

    country_fig.add_trace(go.Choropleth(
        locations=loc_list, z=[1] * len(loc_list),
        colorscale=[[0, row["color"]], [1, row["color"]]], showscale=False, hoverinfo='none'
    ))

    country_fig.add_trace(go.Scattergeo(
        lon=[row["lon"]], lat=[row["lat"]], mode='markers+text',
        text=[f"<b>{row['name']}</b>"], textposition="top center",
        marker=dict(size=10, color='#dc2626'), textfont=dict(size=14, color='#1e293b')
    ))

    country_fig.update_layout(
        template='plotly_white', showlegend=False,
        geo=dict(scope='world', showland=True, landcolor='#f8fafc', showcountries=True, countrycolor='#e2e8f0',
                 center=dict(lat=float(row["lat"]), lon=float(row["lon"])), projection_scale=2.8),
        height=320, margin=dict(l=0, r=0, t=10, b=10)
    )

    return html.Div([
        html.Div([
            dcc.Graph(figure=country_fig, config={'displayModeBar': False})
        ], style={'border': '1px solid #e2e8f0', 'borderRadius': '8px', 'overflow': 'hidden'}),
        html.Hr(style={'borderColor': '#cbd5e1', 'margin': '25px 0'}),
        html.Div(style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', 'gap': '35px'}, children=[
            html.Div(style={'flex': '1', 'minWidth': '300px'}, children=[
                html.Img(src=get_image_base64(row["photo"]),
                         style={'width': '100%', 'maxHeight': '360px', 'objectFit': 'contain',
                                'border': '1px solid #cbd5e1', 'borderRadius': '8px',
                                'background': '#f8fafc'})
            ]),
            html.Div(style={'flex': '2', 'minWidth': '400px'}, children=[
                html.H2(f"{row['name']} Basketball History Archives", style={'color': '#1e3a8a', 'marginTop': '0'}),
                html.Div([
                    html.Strong("Key Influential Figures: ", style={'color': '#b45309', 'fontSize': '16px'}),
                    html.Span(row["leader"], style={'fontSize': '16px', 'fontWeight': 'bold'})
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Strong("Introduction Year: ", style={'color': '#b45309', 'fontSize': '16px'}),
                    html.Span(str(row["start_year"]), style={'fontSize': '16px', 'fontWeight': 'bold'})
                ], style={'marginBottom': '15px'}),

                dcc.Markdown(
                    row["desc"],
                    dangerously_allow_html=True,
                    style={'lineHeight': '1.7', 'fontSize': '15px', 'color': '#334155', 'textAlign': 'justify'}
                )
            ])
        ])
    ])


# ==================== 6. Quiz 测验判断逻辑回调 ====================
@app.callback(
    [Output({'type': 'quiz-feedback', 'index': ALL}, 'children'),
     Output({'type': 'quiz-feedback', 'index': ALL}, 'style'),
     Output('quiz-total-score', 'children')],
    Input('quiz-submit-btn', 'n_clicks'),
    State({'type': 'quiz-options', 'index': ALL}, 'value')
)
def evaluate_quiz(n_clicks, user_answers):
    if n_clicks == 0 or not user_answers:
        empty_feedbacks = [""] * len(quiz_questions)
        empty_styles = [{}] * len(quiz_questions)
        return empty_feedbacks, empty_styles, ""

    feedbacks = []
    styles = []
    correct_count = 0

    for i, q in enumerate(quiz_questions):
        selected = user_answers[i] if i < len(user_answers) else None
        correct = q["answer"]

        if selected == correct:
            correct_count += 1
            feedbacks.append(f"✓ Correct! Perfect answer.")
            styles.append({
                'color': '#15803d', 'backgroundColor': '#dcfce7', 'padding': '10px',
                'borderRadius': '6px', 'fontWeight': 'bold', 'border': '1px solid #86efac'
            })
        else:
            feedbacks.append(f"✗ Incorrect. The correct answer is: {correct}")
            styles.append({
                'color': '#b91c1c', 'backgroundColor': '#fee2e2', 'padding': '10px',
                'borderRadius': '6px', 'fontWeight': 'bold', 'border': '1px solid #fca5a5'
            })

    score_display = f"🎯 Total Score: {correct_count} / {len(quiz_questions)} ({(correct_count / len(quiz_questions)) * 100:.0f}%)"
    return feedbacks, styles, score_display


# ==================== 7. 运行环境启动 ====================
if __name__ == '__main__':
    app.run(debug=True)