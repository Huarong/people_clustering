#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

import test_util

from people_clustering.file_reader import FileReader


class TestFileReader(unittest.TestCase):
    def setUp(self):
        webpages_dir = os.path.join(test_util.ROOT, 'data/weps2007_data_1.1/traininig/web_pages/')
        name = 'Abby_Watkins'
        self.reader = FileReader(webpages_dir, name)

    def tearDown(self):
        del self.reader

    def test_read_webpages(self):
        self.reader.read_webpages()
        first = {'000': {'url': 'http://www.mountainguiding.net/'},
                '001': {'url': 'http://www.thenorthface.com/na/athletes/athletes-AW.html'},
                '002': {'url': 'http://www.bdel.com/community/articles/f03_motherhood.html'},
                '003': {'url': 'http://www.ovariancancer.jhmi.edu/climb/photos.cfm?photo=watkins'},
                '004': {'url': 'http://www.neice.com/Festivales/Festiglace2001/PhotoHTML/Photo3.htm'},
                '005': {'url': 'http://www.escalade.com.au/escalade/1999/watkins.html'},
                '006': {'url': 'http://www.cecbg.com/calendar/jul04cal.htm'},
                '007': {'url': 'http://www.alpinewoman.com/wwwboard/messages/18.html'},
                '008': {'url': 'http://www.vimff.org/speakers.html'},
                '009': {'url': 'http://www.ourayicefestival.com/current_news.htm'},
                '010': {'url': 'http://www.canmoreiceclimbingfestival.com/cast.htm'},
                '011': {'url': 'http://www.planetfear.com/photo_detail.asp?p_id=34'},
                '012': {'url': 'http://www.yamnuska.com/mixed_ice_climbing.html'},
                '013': {'url': 'http://www.ifyouski.com/news/newsarticle/?ObjectID=241515'},
                '014': {'url': 'http://climb.mountainzone.com/2001/mixed/html/index2.html'},
                '015': {'url': 'http://gorp.away.com/gorp/eclectic/jobs/outdoor_jobs2.htm'},
                '016': {'url': 'http://www.womensmountainadventures.com/pages/2/'},
                '017': {'url': 'http://www.iamthewallress.com/yosemitewomen.html'},
                '018': {'url': 'http://www.camp4.com/moreheadlines.php?newsid=60'},
                '019': {'url': 'http://www.cbc.ca/national/news/avalanche/'},
                '020': {'url': 'http://www.penland.org/scholarship.html'},
                '021': {'url': 'http://www.clements.umich.edu/Webguides/UZ/Index_UZ/Watkins.let'},
                '022': {'url': 'http://www.gripped.com/News/29_jun_2004/'},
                '023': {'url': 'http://www.speedclimb.com/yosemite/2nd3rds.htm'},
                '024': {'url': 'http://www.mixeddreams.com/competitions.htm'},
                '025': {'url': 'http://www.csac.org/Incidents/2002-03/20030201-Canada.html'},
                '026': {'url': 'http://www.goldiproductions.com/Pages/comingbackalive/winteravalanche.html'},
                '027': {'url': 'http://bethanie1875.tripod.com/bethanie1875.html'},
                '028': {'url': 'http://www.rock.com.au/rock/backisue.htm'},
                '029': {'url': 'http://www.substancemisuse.net/general-public/gpfeatures/032/page01.htm'},
                '030': {'url': 'http://www.gravsports.com/Gadfly%20Pages/jan_10%20Gadfly.htm'},
                '031': {'url': 'http://www.outdoorindustry.org/press.outdoor.php?news_id=696&sort_year=2004'},
                '032': {'url': 'http://www.jimmychinphotography.com/portfolio_21.htm'},
                '033': {'url': 'http://www.wiredinitiative.com/research-studentprojects.htm'},
                '034': {'url': 'http://www.fishandgame.com/2003articles/91803rei.htm'},
                '035': {'url': 'http://www.passionfruit.com/summer_2000.html'},
                '036': {'url': 'http://www.pharostribune.com/story.asp?id=3646'},
                '037': {'url': 'http://www.rei.com/aboutrei/releases/03climbforlife.html'},
                '038': {'url': 'http://www.cnnsi.com/features/siadventure/24/avalanche/'},
                '039': {'url': 'http://www.makeup4brides.co.uk/brides2.htm'},
                '040': {'url': 'http://www.climbing.com/current/wmnkarakrm/index3.html'},
                '041': {'url': 'http://www.go2rockies.com/businesses/adventurebusiness4.htm'},
                '042': {'url': 'http://vancouverplus.workopolis.com/servlet/Content/qprinter/20030208/UAVALN'},
                '043': {'url': 'http://espn.go.com/xgames/winterx99/iceclimb/ice_difficulty.html'},
                '044': {'url': 'http://expeditionnews.com/Archives/EN_Latest.html'},
                '045': {'url': 'http://www.beyondgravity.com/welcome.htm'},
                '046': {'url': 'http://www.avalanche.org/proc-show.php3?OID=16904'},
                '047': {'url': 'http://www.watkinsfhs.net/cgi-bin/dcguest/dcguest.cgi?marker=81'},
                '048': {'url': 'http://www.sheclimbs.org/sheclimbs_links.html'},
                '049': {'url': 'http://www.califmall.com/XGAMESRESULTS.html'},
                '050': {'url': 'http://www.planetmountain.com/English/Ice/competition/2003/iceresults.html'},
                '051': {'url': 'http://www.erskine.edu/news/06.12.03.html'},
                '052': {'url': 'http://www.sesc.k12.in.us/Cass/sport/Spring/index3.html'},
                '053': {'url': 'http://www.b-g.k12.ky.us/Schools/bghs/activity/fccla/fcclaoff.htm'},
                '054': {'url': 'http://recreation.omniseek.com/news/20000119/081831/Ice_Festival_2000.html'},
                '055': {'url': 'http://www.hilinevideoworks.com/welcome.htm'},
                '056': {'url': 'http://pweb.jps.net/~prichins/womancl.htm'},
                '057': {'url': 'http://www.scn.org/awis/volunteers.htm'},
                '058': {'url': 'http://www.womenclimbing.com/climb/eventdetail.asp?calendarid=329'},
                '059': {'url': 'http://www.boulderweekly.com/archive/011504/elevation.html'},
                '060': {'url': 'http://www.canadianmountainproperty.com/activities/mountaineering.html'},
                '061': {'url': 'http://www.globeandmail.com/servlet/ArticleNews/PEstory/TGAM/20030208/UAVALN/national/national/national_temp/5/5/27/'},
                '062': {'url': 'http://sport.passersbuy.com/sport/photo.html'},
                '063': {'url': 'http://www.wku.edu/news/releases04/june/workshop.html'},
                '064': {'url': 'http://www.cs.colorado.edu/~jrblack/histrec.html'},
                '065': {'url': 'http://westernxc.ckrr.us/results/MaconaquahGirls.htm'},
                '066': {'url': 'http://www.ai.sri.com/~herson/climbing/tr/angel.html'},
                '067': {'url': 'http://www.mountainwoman.com/mountainwoman/news/011602.htm'},
                '068': {'url': 'http://calbears.collegesports.com/sports/w-gym/archive/cal-w-gym-a-atr.html'},
                '069': {'url': 'http://cnews.canoe.ca/CNEWS/Canada/2003/02/03/19781.html'},
                '070': {'url': 'http://www.dyestat.com/9out/us/may/506montco.html'},
                '071': {'url': 'http://www.ifyouski.fr/news/newsarticle/?ObjectID=241515'},
                '072': {'url': 'http://www.ascendingwomen.com/pages/400943/page400943.html?refresh=1080688620760'},
                '073': {'url': 'http://www.cosleyhouston.com/news03-02.htm'},
                '074': {'url': 'http://expn.go.com/etc/s/AXG_X99_results.html'},
                '075': {'url': 'http://www.chickswithpicks.net/guides.htm'},
                '076': {'url': 'http://classic.mountainzone.com/xgames/summer98/climbing/'},
                '077': {'url': 'http://www.chockstone.org/Forum/Forum.asp?Action=DisplayTopic&ForumID=1&MessageID=6413&PagePos=&Sort=&Replies=281&MsgPagePos=220'},
                '078': {'url': 'http://www.outdoornetwork.com/ton_assnnews_archive/2000/12/29/eng-outdoornet-000007/eng-outdoornet-000007_163617_186_931949586142.html'},
                '079': {'url': 'http://www.nextwave.org.au/colony/html/cny_cr000.html'},
                '080': {'url': 'http://www.abcproject.com/journals/sept19.html'},
                '081': {'url': 'http://www.geocities.com/asvcobras/reunion98.htm'},
                '082': {'url': 'http://person.sunmalls.com/'},
                '083': {'url': 'http://www.pocrcadvocates.org/Pages/Feb21.html'},
                '084': {'url': 'http://www.tc.umn.edu/~mulli008/resume.html'},
                '085': {'url': 'http://www.womenwarriors.ca/en/sports/profile.asp?id=69'},
                '086': {'url': 'http://www.kwmap.com/tourism-british-columbia.html'},
                '087': {'url': 'http://www.sporting-goods.ws/sportinggoods/beyond-gravity-video-from-north-face.php'},
                '088': {'url': 'http://www.webcrag.com/events.html'},
                '089': {'url': 'http://www.cityofrevelstoke.com/admin/minutes_2003/minutes02-24-03.htm'},
                '090': {'url': 'http://www.outdooraustralia.com/news_arc/apr03.htm'},
                '091': {'url': 'http://www.kentuckytennis.com/tournaments/tournaments.html?tour=Novice'},
                '092': {'url': 'http://www.listenuptv.com/transcripts/t030403snow.htm'},
                '093': {'url': 'http://www.seracfilms.com/cataract/himcataract1.htm'},
                '094': {'url': 'http://www.onsight.com.au/gallery/overseas/canada/squamish/03.htm'},
                '095': {'url': 'http://www.cliffhanger.com.au/photogallery/window.html?cat=5&photo=1'},
                '096': {'url': 'http://www.sportclimbing.de/news/news.php3?ID=2353&time=03&year=2002&show='},
                '097': {'url': 'http://www.watkins.edu/degree/fineArts/fineArts_facultyStaff.asp'},
                '098': {'url': 'http://www.alardsbigwallclimbing.com/Yosemite.htm'},
                '099': {'url': 'http://westerntrack.ckrr.us/media/05142004.htm'},
                '100': {'url': 'http://www.drkomputing.com/results/olph99.htm'},
                '101': {'url': 'http://www.viewpointswest.com/ImagePages/pG_Lifestyles/0262.htm'},
                '102': {'url': 'http://www.belowzerodigital.com/silenteyes.htm'},
                '103': {'url': 'http://www.sawtoothfilms.com/outside.html'},
                '104': {'url': 'http://climbing.com/press/womensonlymtnexp/'},
                '105': {'url': 'http://www.planetfear.net/climbing/highmountainmag/mountaininfo/1996-1998/Infjul97.htm'},
                '106': {'url': 'http://coshoctonswim.tripod.com/rd5.htm'},
                '107': {'url': 'http://www.saclimb.co.za/articles.html'},
                '108': {'url': 'http://www.sunmalls.com/'},
                '109': {'url': 'http://www.foximas.com/ky/2138550.html'},
                '110': {'url': 'http://www.booksmatter.com/b1585746142.htm'},
                '111': {'url': 'http://ftp.rootsweb.com/pub/usgenweb/va/halifax/vitals/deaths/1857.txt'},
                '112': {'url': 'http://www.nsr-inc.com/canadawest/softgray.htm'},
                '113': {'url': 'http://www.outdoorrelease.com/news_releases/news_detail.asp?ID=898&region=6'},
                '114': {'url': 'http://www.cascadeclimbers.com/threadz/showflat.php/Cat/0/Number/315469/Main/315304'},
                '115': {'url': 'http://alpineclub-edm.org/accidents/accident.asp?id=924'},
                '116': {'url': 'http://www.rockclimbing.com/forums/viewtopic.php?t=41394&start=765'},
                '117': {'url': 'http://www.ledger-enquirer.com/mld/ledgerenquirer/news/5150933.htm'},
                '118': {'url': 'http://www.sports-shopping-online.com/PID-JKskIQQ4/Beyond-Gravity--Video--from-North-Face/'},
                '119': {'url': 'http://communication.students.rmit.edu.au/media/amar_singh/Schneider.html'},
                '120': {'url': 'http://media.passersbuy.com/videodvdmedia/climbing.html'},
                '121': {'url': 'http://forum.powdermag.com/cgi-bin/ultimatebb.cgi?ubb=get_topic;f=1;t=023170;p=2'},
                '122': {'url': 'http://www.tennisinformation.com/rank/5/5/1/3/9/record.asp?id=-4725'},
                '123': {'url': 'http://sunmalls.com/'}}
        second = self.reader.get_description()
        # import pprint
        # pprint.pprint(second)
        self.assertDictEqual(first, second)

if __name__ == '__main__':
    unittest.main()