<?php

/**
 * var IMAGE_FORMAT_PNG
 * defined in zabbix orignal configuration file
 */
define("IMAGE_FORMAT_PNG", 'PNG');

/**
 * Loading zabbix conf file
 */
include(dirname(dirname(__FILE__)) . '/conf/zabbix.conf.php');

// ------------------------------------------------------------------------

/**
 * Customize api of zabbix for anjuke cmdb project
 *
 * zabbix fastApi
 *
 * @package        Api
 * @author        Robanlee@gmail.com
 * @link        http://www.robanlee.com
 */
class fastApi
{

    var $pdh = NULL; //PDO Handler
    var $zabbix_item_names = NULL;

    /**
     * Constructor of fast api
     *
     * @global type $DB
     */
    public function __construct()
    {
        global $DB;
        $autoQuery = 'SET NAMES UTF8';
        $dsn = sprintf("mysql:host=%s;dbname=%s;port=%s", $DB['SERVER'], $DB['DATABASE'], $DB['PORT']
            , array(PDO::MYSQL_ATTR_INIT_COMMAND => $autoQuery));
        $this->pdh = new PDO($dsn, $DB['USER'], $DB['PASSWORD']);

        $this->zabbix_item_names = array(
            'system.cpu.load[percpu,avg1]' => 'cpu_1',
            'system.cpu.load[percpu,avg5]' => 'cpu_5',
            'system.cpu.load[percpu,avg15]' => 'cpu_15',
            'net.if.out[eth0]' => 'net_out',
            'net.if.in[eth0]' => 'net_in',
            'system.cpu.util[,iowait]' => 'iowait',
            'vm.memory.size[available]' => 'available_memory',
            'vm.memory.size[total]' => 'total_memory',
            'iostat[sda,r/s]' => 'sda_read',
            'iostat[sda,w/s]' => 'sda_write'
        );
    }

    public function getAllItems()
    {
        $hostname = $_REQUEST['hostname'];
        if (!$hostname) {
            return jsonRender(-111, 'Parameter error');
        }

        $hosts = ($this->findHostID($hostname));
        if (!count($hosts)) {
            return jsonRender(-117, 'Empty result');
        }

        $hostID = $hosts[$hostname];
        $strSQL = 'select key_,lastvalue as value,prevvalue,from_unixtime(lastclock) as lastclock from items where hostid = ' . $hostID;
        $result = $this->query($strSQL);
        if (!count($result)) {
            return jsonRender(-119, 'empty result');
        }

        $groupResult = array();
        foreach ($result as $idx => $val) {
            $_tmpResult = $val;

            //As float
            if (substr_count($val['value'], '.') == 1) {
                $_tmpResult['value'] = sprintf("%0.2f", $val['value']);
                $_tmpResult['prevvalue'] = sprintf("%0.2f", $val['prevvalue']);
                $_tmpResult['rate'] = ($_tmpResult['prevvalue'] - $_tmpResult['value']);
            }

            if (intval($val['value']) != 0) {
                $_tmpResult['rate'] = sprintf("%0.2f", ($_tmpResult['prevvalue'] / $_tmpResult['value']) / 100);
            }

            if (preg_match('/^(vfs|vm|net)/', $val['key_']) && preg_match('/\d+/', $_tmpResult['value'])) {
                $v = intval($_tmpResult['value']);
                if ($v > 1024 * 1024 * 1024 * 1024) {
                    $v = sprintf('%0.2f', $v / (1024 * 1024 * 1024 * 1024));
                    $_tmpResult['v_unit'] = 'Tb';
                } else if ($v > 1024 * 1024 * 1024 && $v < 1024 * 1024 * 1024 * 1024) {
                    $v = sprintf('%0.2f', $v / (1024 * 1024 * 1024));
                    $_tmpResult['v_unit'] = 'Gb';
                } else if ($v > 1024 * 1024 && v < 1024 * 1024 * 1024) {
                    $v = sprintf('%0.2f', $v / (1024 * 1024));
                    $_tmpResult['v_unit'] = 'Mb';
                } else {
                    //Nothing to do
                }

                $_tmpResult['value'] = $v;
            }

            if (preg_match("/^system/", $_tmpResult['key_'])) {
                $groupResult['system'][] = $_tmpResult;
            } else if (preg_match("/^vfs/", $_tmpResult['key_'])) {
                $groupResult['disk'][] = $_tmpResult;
            } else if (preg_match("/^vm/", $_tmpResult['key_'])) {
                $groupResult['memory'][] = $_tmpResult;
            } else if (preg_match("/^net/", $_tmpResult['key_'])) {
                $groupResult['net'][] = $_tmpResult;
            } else if (preg_match("/^io/", $_tmpResult['key_'])) {
                $groupResult['io'][] = $_tmpResult;
            } else {
                $groupResult['other'][] = $_tmpResult;
            }

        }

        return jsonRender(0, 'OK', $groupResult);
    }

    private function parseValues($arrResult)
    {
        $result = array();
        foreach ($arrResult as $idx => $val) {
            $key = $this->zabbix_item_names[$val['key_']] ? $this->zabbix_item_names[$val['key_']] : $val['key_'];
            if (in_array($key, array('cpu_1', 'cpu_5', 'cpu_15', 'sda_read', 'sda_write'))) {
                $val['value'] = sprintf("%0.2f", $val['value']);
            }

            if (in_array($key, array('free_disk', 'available_memory', 'total_memory', 'total_disk'))) {
                $val['value'] = sprintf("%0.2f", $val['value'] / (1024 * 1024 * 1024));
            }

            if (in_array($key, array('net_out', 'net_in'))) {
                $val['value'] = sprintf("%0.2f", $val['value'] / (1024 * 1024));
            }

            if (in_array($key, array('iowait'))) {
                $val['value'] = sprintf("%0.2f", $val['value']);
            }

            $result[$key] = $val;
        }

        return $result;
    }

    private function findLastItems($hostID)
    {
        $k = "'" . implode("','", array_keys($this->zabbix_item_names)) . "'";
        $strSQL = "SELECT key_,lastvalue as value,from_unixtime(lastclock) as lastclock FROM items where hostid='{$hostID}' and (key_ in ({$k}) or key_ like '%vfs.fs.size%') and lastvalue != '' ";
        $result = $this->query($strSQL);
        if (!count($result)) {
            return array();
        }

        return $this->parseValues($result);
    }

    /**
     * Default route of api
     * @param  string | array hostname
     * @return string | json encoded
     */
    public function index()
    {
        if (!isset($_REQUEST['hostname'])) {
            return jsonRender(-113, 'Paramter hostname must be pass in');
        }

        if (!preg_match('/^[\w\,\s\-]+$/', $_REQUEST['hostname'])) {
            return jsonRender(-115, 'Bad parameter value!');
        }

        $hostname = $_REQUEST['hostname'];

        $hosts = ($this->findHostID($hostname));
        if (!count($hosts)) {
            return jsonRender(-117, 'Empty result');
        }


        $log = $this->findLastItems($hosts[$hostname]);

        $log['available_mem_rate'] = array('value' => 0, 'tm' => date('Y-m-d H:i:s', time()));

        if ($log['available_memory'] && $log['total_memory']) {
            $value = floor(($log['available_memory']['value'] / $log['total_memory']['value']) * 100);
            $log['available_mem_rate']['value'] = $value;
        }

        $i = 0;
        $total = 0;
        $used = 0;
        foreach ($log as $key => $val) {
            if (preg_match('/^vfs/', $key)) {
                $_tmpKey = str_replace(array('vfs.fs.size[', ']'), "", $key);

                list($volumnName, $volumnType) = explode(",", $_tmpKey);

                if ($volumnType != 'pfree') {
                    $val['value'] = $val['value'] / (1024 * 1024 * 1024);
                }


                $val['value'] = sprintf("%0.2f", ($val['value']));
                if ($volumnType == 'total') {
                    $total += $val['value'];
                }

                if ($volumnType == 'used') {
                    $used += $val['value'];
                }

                $_tmpVal = array('key' => $volumnName, 'value' => $val['value']);
                $log['disk'][$volumnName][$volumnType] = $val['value'];

                unset($log[$key]);
            }
        }

        $log['total_disk_used'] = array();
        if ($total > 0 && $used > 0) {
            $log['total_disk_used']['value'] = sprintf("%0.2f", ($used / $total) * 100);
            if ($used >= 1024) {
                $used = sprintf("%0.2fT", $used / 1024);
            } else {
                $used = $used . "G";
            }
            if ($total >= 1024) {
                $total = sprintf("%0.2fT", $total / 1024);
            } else {
                $total = $total . "G";
            }
            $log['total_disk_used']['used'] = $used;
            $log['total_disk_used']['total'] = $total;
            $log['total_disk_used']['key_'] = 'total_disk_used';
        }

        return jsonRender(0, 'OK', $log);
    }

    /**
     * Private function of finding hostid by host name
     * @param type $hostName
     * @return type
     */
    private function findHostID($hostName)
    {
        $aResult = $this->query(sprintf("SELECT hostid,name FROM hosts WHERE name = '%s'", $hostName));
        if (!count($aResult)) {
            return array();
        }

        $aHosts = array();
        foreach ($aResult as $idx => $val) {
            $aHosts[$val['name']] = $val['hostid'];
        }

        return $aHosts;
    }

    /**
     * Finding history via zabbix item name
     * @param type $hostID
     * @return type
     */
    private function findHistory($hostID)
    {
        $k = "'" . implode("','", array_keys($this->zabbix_item_names)) . "'";
        $tmStart = time() - 30 * 60;
        $tmEnd = time() + 30;
        $strSQL = "select h.*,i.key_,date_format(from_unixtime(clock),'%Y-%m-%d %H:%i%s') as tm from history h  left join items i on i.itemid = h.itemid where (clock >= %s and clock < %s) and h.itemid in (select itemid  from items where  hostid = %s and (key_ in (%s)) )  group by h.itemid";
        $strSQL = sprintf($strSQL, $tmStart, $tmEnd, $hostID, $k);
        $result = $this->query($strSQL);
        if (!count($result)) {
            return array();
        }

        return $this->parseValues($result);
    }

    /**
     * Query an result via pdo
     * @param type $strSQL
     * @return type
     */
    private function query($strSQL)
    {
        $sth = $this->pdh->prepare($strSQL);
        $sth->execute();
        return $sth->fetchAll(PDO::FETCH_ASSOC);
    }

    public function details()
    {
        $hostname = $_REQUEST['hostname'];
        $key = $_REQUEST['key'];
        $range = $_REQUEST['range'];
        if(empty($range)){
            $range = 16;
        }else{
            $range = (int)$range;
        }
        if (!$hostname or !$key) {
            return jsonRender(-111, 'Bad parameter');
        }

        $hosts = ($this->findHostID($hostname));
        if (!count($hosts)) {
            return jsonRender(-117, 'Empty result');
        }

        $hostID = $hosts[$hostname];

        if (in_array($key, array('mem'))) {
            $pieResult = $this->renderPieData($hostID, $key);
            return jsonRender(0, 'OK', $pieResult);
        }

        if ($key == 'disk') {
            return $this->findDiskPFree($hostID);
        }

        $table = 'history_uint';

        if (in_array($key, array('system.cpu.util[,iowait]', 'iostat[sda,r/s]', 'iostat[sda,w/s]', 'system.cpu.load[percpu,avg1]'))) {
            $table = 'history';
        }

        $colAlias = 'value';
        //Formatted as GB
        if (in_array($key, array('vm.memory.size[available]', 'vfs.fs.size[/,free]','vm.memory.size[total]'))) {
            $colAlias = 'round(value/(1024*1024*1024),2) as value';
        }

        //Formatted as MB
        if (in_array($key, array('net.if.in[eth0]', 'net.if.out[eth0]'))) {
            $colAlias = 'round(value/(1024*1024),2) as value';
        }

        if (in_array($key, array('system.cpu.util[,iowait]'))) {
            $colAlias = 'round(value,2) as value';
        }


        //Merge statement
        $strSQL = "select date_format(from_unixtime(clock),'%Y-%m-%d %H:%i:%s') as tm, {$colAlias} from {$table}  where itemid =(select itemid from items where hostid= {$hostID} and key_ = '{$key}' )  order by clock desc  limit {$range}";

        $result = $this->query($strSQL);
        return jsonRender(0, 'OK', $result);
    }


    private function findDiskPFree($hostID)
    {
        //$strSQL = "select 'total_disk_pfree', round ( sum(lastvalue) / count(1) ,2) as value , date_format(from_unixtime(lastclock),'%Y-%m-%d %H:%i:%s') as tm  from items where hostid = '{$hostID}' and key_ regexp ('^vfs.fs.size(.*)pfree') and lastvalue != ''";
        $strSQL = "select key_,lastvalue from items where hostid = " . $hostID . " and (key_ in ('vm.memory.size[available]','vm.memory.size[total]') or key_ like 'vfs.fs.size%' )";
        $result = $this->query($strSQL);

        if (!count($result)) {
            return jsonRender();
        }
        $total = 0;
        $used = 0;
        foreach ($result as $val) {
            if (preg_match('/^vfs/', $val['key_'])) {
                $_tmpKey = str_replace(array('vfs.fs.size[', ']'), "", $val['key_']);
                list($volumnName, $volumnType) = explode(",", $_tmpKey);
                if ($volumnType != 'pfree') {
                    $val['lastvalue'] = $val['lastvalue'] / (1024 * 1024 * 1024);
                }
                $val['lastvalue'] = sprintf("%0.2f", ($val['lastvalue']));
                if ($volumnType == 'total') {
                    $total += $val['lastvalue'];
                }
                if ($volumnType == 'used') {
                    $used += $val['lastvalue'];
                }
            }
        }
        $used_ratio = sprintf("%0.2f", ($used / $total) * 100);
        $render = array(array("label" => "可用量", "value" => (100 - $used_ratio)), array("label" => "已使用", "value" => $used_ratio));
        return jsonRender(0, 'OK', $render);
    }

    public function renderPieData($hostID, $type)
    {
        if ($type == 'mem') {
            $key = "'vm.memory.size[available]','vm.memory.size[total]'";
        } else {
            $key = "'vfs.fs.size[/,free]','vfs.fs.size[/,total]'";
        }
        $strSQL = "SELECT key_,lastvalue,from_unixtime(lastclock) as lastclock FROM items where hostid=%s and key_ in (%s)";
        $strSQL = sprintf($strSQL, $hostID, $key);
        $result = $this->query($strSQL);
        if (!count($result)) {
            return array();
        }

        $arrRate = array();
        $lastTime = date("Y-m-d H:i:s", time());
        foreach ($result as $idx => $val) {
            if (in_array($val['key_'], array('vm.memory.size[total]', 'vfs.fs.size[/,total]'))) {
                $arrRate['total'] = $val['lastvalue'];
            } else {
                $arrRate['free'] = $val['lastvalue'];
            }

            $lastTime = $val['lastclock'];
        }

        $free = sprintf("%2d", ($arrRate['free'] / $arrRate['total']) * 100);
        return array(array("label" => "可用量", "value" => $free), array("label" => "已使用", "value" => (100 - $free)));
    }

    /**
     * Default route of api
     * @param  string | array hostname
     * @return string | json encoded
     */
    public function getDataByDay()
    {
        if (!isset($_REQUEST['hostname'])) {
            return jsonRender(-113, 'Paramter hostname must be pass in');
        }

        if (!preg_match('/^[\w\,\s\-]+$/', $_REQUEST['hostname'])) {
            return jsonRender(-115, 'Bad parameter value!');
        }
        $hostname = $_REQUEST['hostname'];
        $hosts = ($this->findHostID($hostname));
        if (!count($hosts)) {
            return jsonRender(-117, 'Empty result');
        }
        $hostid = $hosts[$hostname];
        $k = "'" . implode("','", array_keys($this->zabbix_item_names)) . "'";
        $tmStart = trim($_REQUEST['from']);
        $tmEnd = trim($_REQUEST['end']);
        $strSQL = "select h.clock,h.value ,i.key_  from history_uint  h left join items i on i.itemid = h.itemid where (clock >= " . $tmStart . " and clock < " . $tmEnd . ") and h.itemid in (select itemid  from items where  hostid = " . $hostid . " and (key_ in (" . $k . ")) ) order by h.clock asc";
        $result = $this->query($strSQL);
        if (!count($result)) {
            return array();
        }
        jsonRender(0, 'OK', $result);
    }

    public function getHostIdByHostname(){
        $hostname = $_REQUEST['hostname'];
        $result = $this->findHostID($hostname);
        jsonRender(0, 'OK', $result);
    }

}


function jsonRender($code = 0, $msg = 'OK', $data = array())
{
    echo json_encode(array('code' => $code, 'msg' => $msg, 'data' => $data));
    exit;
}

$action = isset($_REQUEST['act']) ? trim($_REQUEST['act']) : 'index';
$clazz = new fastApi();

if (!method_exists($clazz, $action)) {
    return jsonRender(-110, 'Action not exists!');
}

$clazz->$action();

