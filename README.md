# FWAdmin

In the current alpha version, FWadmin allows to build EDLs referenced by firewalls. EDLs can be permanent, related to time-window frames or requested by users.

Components:

* DeviceGroup objects are a groups of Netbox devices.
* DynamicList objects are a group of DeviceGroup objects. They can be permanent (always on), related to time windows, or user requests. DynamicList objects build the EDL referenced by firewalls. Protocol, port and application are specified in the firewall rule referencing the EDL.
* Users can create Request objects for a specifc time frame referencing DynamicList objects.

How to use it:

On Netbox

Configure the firewall on netbox fwadmin with username and password.
Configure devices with interfaces and ipaddresses
Create device groups
Create EDL with name, device groups, firewalls, rule name, direction???
Grab the EDL URL


Configure a new admin role in Device -> Admin Roles

   admin-role {
      session-fence {
        role {
          device {
            webui;
            xmlapi {
              op enable;
            }
          }
        }
        description "Terminate traffic sessions";
      }

Add an admin user with the above role.

Generate a token

curl -k -X GET 'https://<firewall>/api/?type=keygen&user=<username>&password=<password>'

https://127.0.0.1:8443/api/?type=keygen&user=netbox&password=netbox

<response status="success">
<result>
<key>
LUFRPT1rUnZlM3lHeXhSRzI4MGNVY0ZCK3NxMUtRbkU9YkFRQjV1Sm9BK0tGeTA5QXNqL29ka0NOTFZIYjdadERicDkxOWhUeFNRcEtHOFFQSUtydFl5UGk5VW9SYmlCdA==
</key>
</result>
</response>






IF HTTPS IS USED:
Configure a certificate profile in Device -> Certificate Management -> Certificate Profile according to your security policies.



Create EDL on Objects -> External Dynamic Lists
Name: Server-to-DMZ
Type: IP List
Source: the link grabbed before
Check for updates: 5 minutes (if different, please update netbox congiruation)



Debug on PANOS

admin@PA-VM> request system external-list refresh type ip name Server-to-DMZ

EDL refresh job enqueued

admin@PA-VM> show jobs all

Enqueued              Dequeued           ID  PositionInQ                              Type                         Status Result Completed
------------------------------------------------------------------------------------------------------------------------------------------
2023/05/19 03:57:02   03:57:02           43                                     EDLRefresh                            ACT   PEND        55%


admin@PA-VM> show jobs all

Enqueued              Dequeued           ID  PositionInQ                              Type                         Status Result Completed
------------------------------------------------------------------------------------------------------------------------------------------
2023/05/19 03:29:48   03:29:48           33                                     EDLRefresh                            FIN     OK 03:29:57

admin@PA-VM> request system external-list show type ip name Server-to-DMZ

Server-to-DMZ
        Total valid entries     : 1
        Total ignored entries   : 0
        Total invalid entries   : 0
        Total displayed entries : 1
        Valid ips:
                192.168.192.25/32



admin@PA-VM> show session all filter rule Server-Any-to-DMZ-EDL

No Active Sessions




Testing user profile:

https://127.0.0.1:8443/php/rest/browse.php/op::clear::session


>>> url
'https://172.29.129.64/api/?type=op&cmd=<clear><session><all><filter><rule>Server-Any-to-DMZ-EDL</rule></filter></all></session></clear>&key=LUFRPT1rUnZlM3lHeXhSRzI4MGNVY0ZCK3NxMUtRbkU9YkFRQjV1Sm9BK0tGeTA5QXNqL29ka0NOTFZIYjdadERicDkxOWhUeFNRcEtHOFFQSUtydFl5UGk5VW9SYmlCdA=='
>>> r = requests.get(url, verify=False)
>>> r.status_code
200
>>> r.text
'<response status="success"><result>\n  <member>sessions cleared</member>\n</result></response>'



admin@PA-VM> show session all filter rule Server-Any-to-DMZ-EDL

--------------------------------------------------------------------------------
ID          Application    State   Type Flag  Src[Sport]/Zone/Proto (translated IP[Port])
Vsys                                          Dst[Dport]/Zone (translated IP[Port])
--------------------------------------------------------------------------------
323          ssh            ACTIVE  FLOW       192.168.193.25[39686]/Server/6  (192.168.193.25[39686])
vsys1                                          192.168.192.25[22]/DMZ  (192.168.192.25[22])




clear session all filter rule Server-Any-to-DMZ-EDL


admin@PA-VM> clear session all filter rule Server-Any-to-DMZ-EDL

sessions cleared



development

postgres

ALTER USER user_name CREATEDB;



tODO:

test completo (sessione funzionante, connessione, sessione che scade, fencing del firewall).
